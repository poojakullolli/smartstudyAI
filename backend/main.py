<<<<<<< HEAD
import os
import threading
import time
import logging
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
import schedule

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base, SessionLocal
from backend.routers import auth, planner, tracker, explainer
from backend.auth_utils import get_current_user
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models
from backend.ai_utils import analyze_weak_subjects
from fastapi import Depends, HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# 🔥 Load Environment Variables FIRST
# ─────────────────────────────────────────────
load_dotenv()   # This loads your .env file

print("GOOGLE_CLIENT_ID:", os.getenv("GOOGLE_CLIENT_ID"))
print("GOOGLE_CLIENT_SECRET:", os.getenv("GOOGLE_CLIENT_SECRET"))


# ─────────────────────────────────────────────
# 🔥 Firebase Initialization
# ─────────────────────────────────────────────
def init_firebase():
    if not firebase_admin._apps:
        base_dir = os.path.dirname(__file__)
        candidates = [
            os.path.join(base_dir, "firebase_key.json"),
            os.path.join(base_dir, "firebase_key.json.json"),
        ]
        key_file = next((f for f in candidates if os.path.exists(f)), None)

        if key_file:
            cred = credentials.Certificate(key_file)
            firebase_admin.initialize_app(cred)
            print(f"[Firebase] Initialized with key: {os.path.basename(key_file)}")
        else:
            print(
                "[Firebase] WARNING: No service account key file found. "
                "Place firebase_key.json inside backend/ folder."
            )


init_firebase()


# ─────────────────────────────────────────────
# Create SQLAlchemy tables
# ─────────────────────────────────────────────
Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────
app = FastAPI(title="SmartStudy AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────
=======
from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers import auth, planner, tracker, explainer

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Study Planner API")

>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
app.include_router(auth.router)
app.include_router(planner.router)
app.include_router(tracker.router)
app.include_router(explainer.router)

<<<<<<< HEAD

@app.get("/")
def read_root():
    return {"message": "Welcome to the SmartStudy AI API!", "status": "online"}

def get_badge_info(xp_points: int):
    badges = [
        (0, "🌱", "Newcomer", "#6b7280"),
        (100, "✨", "Novice", "#10b981"),
        (300, "🔥", "Scholar", "#f59e0b"),
        (600, "⭐", "Expert", "#3b82f6"),
        (1000, "💎", "Master", "#8b5cf6"),
        (1500, "👑", "Legend", "#ef4444"),
        (2500, "🏆", "Champion", "#ec4899")
    ]
    
    for threshold, icon, name, color in reversed(badges):
        if xp_points >= threshold:
            next_badge = next(((t, i, n, c) for t, i, n, c in badges if t > threshold), None)
            return {
                "badge_icon": icon,
                "badge_name": name,
                "badge_color": color,
                "next_badge": next_badge[1] if next_badge else None,
                "next_badge_threshold": next_badge[0] if next_badge else None,
                "next_badge_progress": xp_points / next_badge[0] if next_badge else 100
            }


def reset_weekly_xp():
    """Reset weekly XP for all users every Sunday"""
    db = SessionLocal()
    try:
        users_updated = db.query(models.User).update({models.User.weekly_xp: 0})
        db.commit()
        logger.info(f"[SCHEDULER] Weekly XP reset completed. {users_updated} users updated.")
    except Exception as e:
        logger.error(f"[SCHEDULER] Error resetting weekly XP: {e}")
        db.rollback()
    finally:
        db.close()


def run_scheduler():
    """Run background scheduler in separate thread"""
    schedule.every().sunday.at("00:00").do(reset_weekly_xp)
    
    logger.info("[SCHEDULER] Weekly XP reset scheduler started (runs every Sunday at 00:00)")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

@app.get("/user/stats")
def get_user_stats(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.refresh(current_user)
    xp_current = current_user.xp_points % 100
    xp_next = 100
    
    badge_info = get_badge_info(int(current_user.xp_points))
    
    response = {
        "level": current_user.level,
        "xp_points": current_user.xp_points,
        "xp_current": xp_current,
        "xp_next": xp_next,
        "xp_percentage": (xp_current / xp_next) * 100
    }
    response.update(badge_info)
    
    return response

@app.get("/analytics/study-pattern")
def get_study_pattern(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import func, desc, extract
    from datetime import datetime, timedelta
    
    sessions = db.query(models.StudySession).filter(
        models.StudySession.user_id == current_user.id
    ).all()
    
    if not sessions:
        return {
            "most_studied_subject": None,
            "least_studied_subject": None,
            "average_daily_minutes": 0,
            "most_productive_hour": None,
            "weekly_data": [0]*7,
            "total_sessions": 0,
            "total_minutes": 0
        }
    
    # Most/Least studied subject
    subject_stats = db.query(
        models.StudySession.subject,
        func.sum(models.StudySession.duration_minutes).label("total")
    ).filter(models.StudySession.user_id == current_user.id)\
     .group_by(models.StudySession.subject)\
     .order_by(desc("total")).all()
    
    most_studied = subject_stats[0].subject if subject_stats else None
    least_studied = subject_stats[-1].subject if len(subject_stats) > 1 else None
    
    # Average daily study time
    days_ago = (datetime.utcnow() - sessions[0].completed_at).days + 1
    total_minutes = sum(s.duration_minutes for s in sessions)
    avg_daily = total_minutes / max(days_ago, 1)
    
    # Most productive hour
    hour_stats = db.query(
        extract('hour', models.StudySession.completed_at).label("hour"),
        func.count(models.StudySession.id).label("count")
    ).filter(models.StudySession.user_id == current_user.id)\
     .group_by("hour")\
     .order_by(desc("count")).first()
    
    most_productive_hour = int(hour_stats.hour) if hour_stats else None
    
    # Weekly data (last 7 days)
    weekly_data = []
    for i in range(6, -1, -1):
        date = datetime.utcnow().date() - timedelta(days=i)
        day_minutes = db.query(func.sum(models.StudySession.duration_minutes))\
            .filter(
                models.StudySession.user_id == current_user.id,
                func.date(models.StudySession.completed_at) == date
            ).scalar() or 0
        weekly_data.append(int(day_minutes))
    
    return {
        "most_studied_subject": most_studied,
        "least_studied_subject": least_studied,
        "average_daily_minutes": round(avg_daily, 1),
        "most_productive_hour": most_productive_hour,
        "weekly_data": weekly_data,
        "total_sessions": len(sessions),
        "total_minutes": total_minutes
    }

@app.post("/ai/weak-analysis")
def get_weak_analysis(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import func, desc, extract
    from datetime import datetime, timedelta
    
    sessions = db.query(models.StudySession).filter(
        models.StudySession.user_id == current_user.id
    ).all()
    
    # Get study pattern data
    subject_stats = db.query(
        models.StudySession.subject,
        func.sum(models.StudySession.duration_minutes).label("total")
    ).filter(models.StudySession.user_id == current_user.id)\
     .group_by(models.StudySession.subject)\
     .order_by(desc("total")).all()
    
    most_studied = subject_stats[0].subject if subject_stats else None
    least_studied = subject_stats[-1].subject if len(subject_stats) > 1 else None
    
    total_minutes = sum(s.duration_minutes for s in sessions) if sessions else 0
    days_ago = (datetime.utcnow() - sessions[0].completed_at).days + 1 if sessions else 1
    avg_daily = total_minutes / max(days_ago, 1)
    
    study_data = {
        "most_studied_subject": most_studied,
        "least_studied_subject": least_studied,
        "average_daily_minutes": round(avg_daily, 1),
        "total_sessions": len(sessions),
        "total_minutes": total_minutes
    }
    
    analysis = analyze_weak_subjects(study_data)
    return {"analysis": analysis}


@app.get("/leaderboard/global")
def get_global_leaderboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import func, desc
    
    # Get top 50 users
    top_users = db.query(
        models.User.id,
        models.User.email,
        models.User.total_xp,
        models.User.level,
        models.User.streak
    ).order_by(desc(models.User.total_xp)).limit(50).all()
    
    # Find current user's rank
    user_rank = db.query(models.User).filter(
        models.User.total_xp > current_user.total_xp
    ).count() + 1
    
    leaderboard = []
    for i, user in enumerate(top_users):
        badge = get_badge_info(int(user.total_xp))
        leaderboard.append({
            "rank": i + 1,
            "email": user.email,
            "total_xp": user.total_xp,
            "level": user.level,
            "streak": user.streak,
            "badge_icon": badge["badge_icon"],
            "badge_name": badge["badge_name"],
            "badge_color": badge["badge_color"]
        })
    
    return {
        "leaderboard": leaderboard,
        "user_rank": user_rank,
        "user_xp": current_user.total_xp,
        "user_level": current_user.level
    }


@app.get("/leaderboard/weekly")
def get_weekly_leaderboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from sqlalchemy import func, desc
    
    # Get top 50 users
    top_users = db.query(
        models.User.id,
        models.User.email,
        models.User.weekly_xp,
        models.User.level,
        models.User.streak
    ).order_by(desc(models.User.weekly_xp)).limit(50).all()
    
    # Find current user's rank
    user_rank = db.query(models.User).filter(
        models.User.weekly_xp > current_user.weekly_xp
    ).count() + 1
    
    leaderboard = []
    for i, user in enumerate(top_users):
        badge = get_badge_info(int(user.weekly_xp))
        leaderboard.append({
            "rank": i + 1,
            "email": user.email,
            "weekly_xp": user.weekly_xp,
            "level": user.level,
            "streak": user.streak,
            "badge_icon": badge["badge_icon"],
            "badge_name": badge["badge_name"],
            "badge_color": badge["badge_color"]
        })
    
    return {
        "leaderboard": leaderboard,
        "user_rank": user_rank,
        "user_xp": current_user.weekly_xp,
        "user_level": current_user.level
    }


@app.post("/challenge/create")
def create_challenge(
    opponent_email: str,
    goal: str,
    duration_days: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from datetime import datetime, timedelta
    
    # Find opponent
    opponent = db.query(models.User).filter(models.User.email == opponent_email).first()
    if not opponent:
        raise HTTPException(status_code=404, detail="User not found")
    
    if opponent.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot challenge yourself")
    
    # Check for existing active challenge
    existing = db.query(models.Challenge).filter(
        ((models.Challenge.challenger_id == current_user.id) & (models.Challenge.opponent_id == opponent.id)) |
        ((models.Challenge.challenger_id == opponent.id) & (models.Challenge.opponent_id == current_user.id)),
        models.Challenge.status.in_(["pending", "active"])
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Active challenge already exists with this user")
    
    # Create challenge
    expires_at = datetime.utcnow() + timedelta(days=duration_days)
    challenge = models.Challenge(
        challenger_id=current_user.id,
        opponent_id=opponent.id,
        goal=goal,
        duration_days=duration_days,
        challenger_start_xp=current_user.total_xp,
        expires_at=expires_at
    )
    
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    
    return {"message": "Challenge sent successfully", "challenge_id": challenge.id}


@app.post("/challenge/accept")
def accept_challenge(
    challenge_id: int,
    accept: bool,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    challenge = db.query(models.Challenge).filter(
        models.Challenge.id == challenge_id,
        models.Challenge.opponent_id == current_user.id,
        models.Challenge.status == "pending"
    ).first()
    
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    if accept:
        challenge.status = "active"
        challenge.opponent_start_xp = current_user.total_xp
    else:
        challenge.status = "cancelled"
    
    db.commit()
    return {"message": "Challenge updated successfully"}


@app.get("/challenge/status")
def get_challenges(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import datetime
    
    challenges = db.query(models.Challenge).filter(
        (models.Challenge.challenger_id == current_user.id) |
        (models.Challenge.opponent_id == current_user.id)
    ).order_by(models.Challenge.created_at.desc()).all()
    
    result = []
    for c in challenges:
        # Auto-check winner if active and expired
        if c.status == "active" and datetime.utcnow() > c.expires_at:
            challenger_gain = c.challenger.total_xp - c.challenger_start_xp
            opponent_gain = c.opponent.total_xp - c.opponent_start_xp
            
            if challenger_gain > opponent_gain:
                c.winner_id = c.challenger_id
            elif opponent_gain > challenger_gain:
                c.winner_id = c.opponent_id
            else:
                c.winner_id = None  # Tie
            
            c.status = "completed"
            db.commit()
        
        challenger_gain = c.challenger.total_xp - c.challenger_start_xp if c.challenger_start_xp else 0
        opponent_gain = c.opponent.total_xp - c.opponent_start_xp if c.opponent_start_xp else 0
        
        result.append({
            "id": c.id,
            "challenger_email": c.challenger.email,
            "opponent_email": c.opponent.email,
            "goal": c.goal,
            "duration_days": c.duration_days,
            "status": c.status,
            "challenger_gain": challenger_gain,
            "opponent_gain": opponent_gain,
            "winner_email": c.winner.email if c.winner_id else None,
            "expires_at": c.expires_at.isoformat(),
            "created_at": c.created_at.isoformat(),
            "is_opponent": c.opponent_id == current_user.id
        })
    
    return result


# ─────────────────────────────────────────────
# Start background scheduler
# ─────────────────────────────────────────────
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# ─────────────────────────────────────────────
# Run App
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8042, reload=True)
=======
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Study Planner API!"}
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
