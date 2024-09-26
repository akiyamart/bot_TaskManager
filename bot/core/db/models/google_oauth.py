from sqlalchemy import Column, Integer, Enum, ForeignKey, TIMESTAMP, String
from datetime import datetime

from .base import Model

class GoogleOAuth(Model):
    __tablename__ = 'google_oauth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(String, nullable=False)
    private_key_id = Column(String, nullable=False)
    private_key = Column(String, nullable=False) 
    client_email = Column(String, nullable=False)
    client_id = Column(String, nullable=False)
    auth_uri = Column(String, nullable=False)
    token_uri = Column(String, nullable=False)
    auth_provider_x509_cert_url = Column(String, nullable=False)
    client_x509_cert_url = Column(String, nullable=False)
    universe_domain = Column(String, nullable=False)

    def __repr__(self):
        return f"<GoogleOAuth(user_id={self.user_id}, notification_type={self.notification_type.value}, created_at={self.created_at})>"
