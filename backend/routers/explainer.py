from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas
from backend.auth_utils import get_current_user
from backend.ai_utils import explain_doubt

router = APIRouter(prefix="/explainer", tags=["explainer"])

@router.post("/explain", response_model=schemas.DoubtResponse)
def doubt_explain(request: schemas.DoubtRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    answer = explain_doubt(question=request.question, difficulty=request.difficulty)
    
    # Save history
    new_doubt = models.DoubtHistory(
        question=request.question,
        answer=answer,
        difficulty=request.difficulty,
        user_id=current_user.id
    )
    db.add(new_doubt)
<<<<<<< HEAD
    
    # Award XP for AI session completion
    from datetime import datetime, date, timedelta
    
    current_user.xp_points += 20
    current_user.total_xp += 20
    current_user.weekly_xp += 20
    current_user.level = current_user.xp_points // 100 + 1
    
    # Update streak
    today = date.today()
    last_date = current_user.last_study_date
    
    if last_date == today:
        # Already studied today, no streak change
        pass
    elif last_date == today - timedelta(days=1):
        # Consecutive day
        current_user.streak += 1
    else:
        # New streak
        current_user.streak = 1
    current_user.last_study_date = today
    
    db.commit()
    db.refresh(new_doubt)
    db.refresh(current_user)
=======
    db.commit()
    db.refresh(new_doubt)
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    
    return {"question": request.question, "answer": answer}

@router.get("/history")
def get_doubt_history(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    history = db.query(models.DoubtHistory).filter(models.DoubtHistory.user_id == current_user.id).order_by(models.DoubtHistory.created_at.desc()).all()
    return history
