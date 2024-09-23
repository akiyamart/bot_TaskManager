from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP
from datetime import datetime
import enum

from .base import Model

class ActionType(enum.Enum):
    create_task = "create_task"
    delete_task = "delete_task"
    update_task = "update_task"
    complete_task = "complete_task"

class ActionLog(Model):
    __tablename__ = 'action_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True) 
    action = Column(Enum(ActionType), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.now)  

    def __repr__(self):
        return f"<ActionLog(user_id={self.user_id}, action={self.action.value}, timestamp={self.timestamp})>"
