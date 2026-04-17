from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserDisplay(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class StudyPlanBase(BaseModel):
    subject: str
    exam_date: date
    daily_available_hours: float
    is_weak_subject: bool
    is_completed: bool = False

class StudyPlanCreate(StudyPlanBase):
    pass

class StudyPlanDisplay(StudyPlanBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ScheduleBlock(BaseModel):
    start: str
    end: str
    task: str

class PlannerDashboardInfo(BaseModel):
    plans: List[StudyPlanDisplay]
    schedule: List[ScheduleBlock]
    progress_percentage: float

class TaskBase(BaseModel):
    subject: str
    topic: str
    duration_minutes: int
    is_completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True

class DoubtRequest(BaseModel):
    question: str
    difficulty: str

class DoubtResponse(BaseModel):
    question: str
    answer: str

class DoubtHistoryDisplay(BaseModel):
    id: int
    question: str
    answer: str
    difficulty: str
    created_at: datetime

    class Config:
        from_attributes = True
