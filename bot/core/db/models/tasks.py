from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum, TIMESTAMP, Interval
from datetime import datetime
import enum

from .base import Model

class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    canceled = "canceled"

class Task(Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    created_at = Column(TIMESTAMP, default=datetime.now)
    due_date = Column(TIMESTAMP, nullable=True)
    duration = Column(Interval, nullable=True)

    def __repr__(self):
        return f"<Task(title={self.title}, status={self.status.value})>"
