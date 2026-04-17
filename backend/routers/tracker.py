from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas
from backend.auth_utils import get_current_user

router = APIRouter(prefix="/tracker", tags=["tracker"])

@router.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.user_id == current_user.id).all()

@router.post("/tasks", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = models.Task(**task.model_dump(), user_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def complete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
<<<<<<< HEAD
    
    was_completed = task.is_completed
    task.is_completed = not task.is_completed
    
    # Award XP when task is completed
    if task.is_completed and not was_completed:
        from datetime import datetime, date, timedelta
        
        # Update XP
        current_user.xp_points += 10
        current_user.total_xp += 10
        current_user.weekly_xp += 10
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
        
        # Track study session
        study_session = models.StudySession(
            user_id=current_user.id,
            subject=task.subject,
            duration_minutes=task.duration_minutes
        )
        db.add(study_session)
    
    db.commit()
    db.refresh(task)
    db.refresh(current_user)
=======
    task.is_completed = not task.is_completed
    db.commit()
    db.refresh(task)
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

@router.get("/progress")
def get_progress(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.is_completed])
    total_hours = sum([t.duration_minutes for t in tasks if t.is_completed]) / 60
    
    percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Simple motivation logic
    if percentage == 0:
        motivation = "Let's get started! Planning is half the battle won."
    elif percentage < 50:
        motivation = "You're making progress. Keep pushing!"
    elif percentage < 100:
        motivation = "Almost there! Don't stop now."
    else:
        motivation = "Amazing job! You finished all your tasks."
        
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "total_hours": round(total_hours, 2),
        "percentage": round(percentage, 2),
        "motivation": motivation
    }
