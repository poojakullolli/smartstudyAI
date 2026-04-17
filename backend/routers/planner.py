from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas, auth_utils
from datetime import date, datetime, timedelta

router = APIRouter(prefix="/planner", tags=["planner"])

@router.post("/create", response_model=schemas.StudyPlanDisplay)
def create_plan(plan: schemas.StudyPlanCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth_utils.get_current_user)):
    new_plan = models.StudyPlan(**plan.model_dump(), user_id=current_user.id)
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

@router.get("/my-plans", response_model=schemas.PlannerDashboardInfo)
def get_my_plans(db: Session = Depends(get_db), current_user: models.User = Depends(auth_utils.get_current_user)):
    plans = db.query(models.StudyPlan).filter(models.StudyPlan.user_id == current_user.id).all()
    
    total_plans = len(plans)
    completed_plans = sum(1 for p in plans if p.is_completed)
    progress_percentage = (completed_plans / total_plans * 100) if total_plans > 0 else 0.0

    schedule = []
    if total_plans > 0:
        # User defined max free time input assumption from their plans:
        daily_hours = max(p.daily_available_hours for p in plans)
        total_minutes = int(daily_hours * 60)
        
        weights = {}
        total_weight = 0
        active_plans = [p for p in plans if not p.is_completed]
        
        for p in active_plans:
            weight = 1.0
            if p.is_weak_subject:
                weight += 0.40
            
            days_to_exam = (p.exam_date - date.today()).days
            if 0 <= days_to_exam <= 7:
                weight += 2.0
                
            weights[p.id] = weight
            total_weight += weight
            
        current_time = datetime.strptime("09:00", "%H:%M")
        
        if active_plans and total_minutes > 0:
            for p in active_plans:
                subject_minutes = int(total_minutes * (weights[p.id] / total_weight))
                
                while subject_minutes > 0:
                    block_minutes = min(50, subject_minutes)
                    if block_minutes < 15 and subject_minutes < 15: # Ignore negligible fractions
                        break
                        
                    end_time = current_time + timedelta(minutes=block_minutes)
                    
                    schedule.append(schemas.ScheduleBlock(
                        start=current_time.strftime("%H:%M"),
                        end=end_time.strftime("%H:%M"),
                        task=p.subject
                    ))
                    
                    subject_minutes -= block_minutes
                    current_time = end_time
                    
                    # 10 min break after every block (unless this is literally the end)
                    if subject_minutes > 0 or p != active_plans[-1]:
                        break_end_time = current_time + timedelta(minutes=10)
                        schedule.append(schemas.ScheduleBlock(
                            start=current_time.strftime("%H:%M"),
                            end=break_end_time.strftime("%H:%M"),
                            task="Break"
                        ))
                        current_time = break_end_time
            
            rev_start = current_time
            rev_end = rev_start + timedelta(minutes=30)
            schedule.append(schemas.ScheduleBlock(
                        start=rev_start.strftime("%H:%M"),
                        end=rev_end.strftime("%H:%M"),
                        task="Daily Revision"
            ))
            
    return schemas.PlannerDashboardInfo(
        plans=plans,
        schedule=schedule,
        progress_percentage=progress_percentage
    )

@router.delete("/delete/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth_utils.get_current_user)):
    plan = db.query(models.StudyPlan).filter(models.StudyPlan.id == plan_id, models.StudyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(plan)
    db.commit()
    return None

@router.put("/toggle-complete/{plan_id}", response_model=schemas.StudyPlanDisplay)
def toggle_complete(plan_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth_utils.get_current_user)):
    plan = db.query(models.StudyPlan).filter(models.StudyPlan.id == plan_id, models.StudyPlan.user_id == current_user.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan.is_completed = not plan.is_completed
    db.commit()
    db.refresh(plan)
    return plan
