from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
<<<<<<< HEAD
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    xp_points = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    weekly_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    streak = Column(Integer, default=0)
    last_study_date = Column(Date, nullable=True)
=======
    hashed_password = Column(String, nullable=False)
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124

    plans = relationship("StudyPlan", back_populates="owner")
    tasks = relationship("Task", back_populates="owner")
    doubts = relationship("DoubtHistory", back_populates="owner")

class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String, nullable=False)
    exam_date = Column(Date, nullable=False)
    daily_available_hours = Column(Float, nullable=False)
    is_weak_subject = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="plans")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    duration_minutes = Column(Integer, default=60)
    is_completed = Column(Boolean, default=False)
    date = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="tasks")

class DoubtHistory(Base):
    __tablename__ = "doubt_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="doubts")
<<<<<<< HEAD

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    challenger_id = Column(Integer, ForeignKey("users.id"))
    opponent_id = Column(Integer, ForeignKey("users.id"))
    goal = Column(String, nullable=False)  # "xp", "tasks", "hours"
    duration_days = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # pending, active, completed, cancelled
    challenger_start_xp = Column(Integer, default=0)
    opponent_start_xp = Column(Integer, default=0)
    winner_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    challenger = relationship("User", foreign_keys=[challenger_id])
    opponent = relationship("User", foreign_keys=[opponent_id])
=======
>>>>>>> c41cad1c30704f98dab208e9206dad75a002b124
