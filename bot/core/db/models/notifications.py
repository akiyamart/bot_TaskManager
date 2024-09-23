from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP, String
from datetime import datetime
import enum

from .base import Model

class NotificationType(enum.Enum):
    task_reminder = "task_reminder"  
    daily_summary = "daily_summary" 
    overdue_alert = "overdue_alert" 
    custom_notification = "custom_notification"  

class Notification(Model):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False) 
    created_at = Column(TIMESTAMP, default=datetime.now)  
    content = Column(String(255), nullable=True)  

    def __repr__(self):
        return f"<Notification(user_id={self.user_id}, notification_type={self.notification_type.value}, created_at={self.created_at})>"
