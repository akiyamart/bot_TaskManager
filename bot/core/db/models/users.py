from sqlalchemy import Column, Integer, String, TIMESTAMP
from datetime import datetime

from .base import Model

class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    google_api_key = Column(String(255))

    def __repr__(self):
        return f"<User(nid={self.id}\ncreated_at={self.created_at}\n)>"
