from sqlalchemy import Column, String, Text, Integer, ForeignKey, TIMESTAMP, UUID
from datetime import datetime
import uuid

from .base import Model

class Task(Model):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now())
    due_date = Column(TIMESTAMP, nullable=True)
    start_time = Column(TIMESTAMP, nullable=True)
    end_time = Column(TIMESTAMP, nullable=True)
    reminder_time = Column(TIMESTAMP, nullable=True)

    def __repr__(self):
        return f"<Task(title={self.title}, status={self.status.value})>"
