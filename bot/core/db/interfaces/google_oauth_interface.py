from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete
from typing import Union, Dict

from ..models import GoogleOAuth

class GoogleOAuthDAL:
    def __init__(self, db_connect: AsyncSession):
        self.db_connect = db_connect

    async def add_data(self,
            user_id: int, project_id: str, private_key_id: str, private_key: str, client_email: str,
            client_id: str, auth_uri: str, token_uri: str, auth_provider_x509_cert_url: str, 
            client_x509_cert_url: str, universe_domain: str
        ) -> GoogleOAuth:

        data = GoogleOAuth(
            user_id=user_id, project_id=project_id, private_key_id=private_key_id, private_key=private_key,
            client_email=client_email, client_id=client_id, auth_uri=auth_uri, token_uri=token_uri,
            auth_provider_x509_cert_url=auth_provider_x509_cert_url, client_x509_cert_url=client_x509_cert_url,
            universe_domain=universe_domain
        )

        self.db_connect.add(data)
        await self.db_connect.flush()
        return data
    
    async def update_data(self, user_id: int,
            project_id: str, private_key_id: str,
            private_key: str, client_email: str,
            client_id: str, auth_uri: str,
            token_uri: str, auth_provider_x509_cert_url: str,
            client_x509_cert_url: str, universe_domain: str
        ) -> GoogleOAuth:
        
        existing_data = await self.db_connect.execute(
            select(GoogleOAuth).where(GoogleOAuth.user_id == user_id)
        )
        google_oauth = existing_data.scalars().first()

        if not google_oauth:
            raise ValueError("User not found")

        google_oauth.project_id = project_id
        google_oauth.private_key_id = private_key_id
        google_oauth.private_key = private_key
        google_oauth.client_email = client_email
        google_oauth.client_id = client_id
        google_oauth.auth_uri = auth_uri
        google_oauth.token_uri = token_uri
        google_oauth.auth_provider_x509_cert_url = auth_provider_x509_cert_url
        google_oauth.client_x509_cert_url = client_x509_cert_url
        google_oauth.universe_domain = universe_domain

        await self.db_connect.flush()
        return google_oauth
    
    async def get_data(self, user_id) -> GoogleOAuth:
        stmt = select(GoogleOAuth).where(GoogleOAuth.user_id == user_id)
        result = await self.db_connect.execute(stmt)
        return result.scalars().first()     

    async def delete_data(self, user_id: int) -> bool:
        stmt = delete(GoogleOAuth).where(GoogleOAuth.user_id == user_id)
        result = await self.db_connect.execute(stmt)
        return result.rowcount > 0
