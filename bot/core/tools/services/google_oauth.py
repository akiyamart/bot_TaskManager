from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from ...schemas import GoogleOAuthCreate, ShowGoogleOAuthResponse, GoogleOAuthDelete
from ...db.interfaces import GoogleOAuthDAL

async def update_google_oauth_data(body: GoogleOAuthCreate, db: AsyncSession) -> Union[ShowGoogleOAuthResponse, None]:
    async with db.begin():
        google_oauth_dal = GoogleOAuthDAL(db)

        action = google_oauth_dal.add_data

        if await google_oauth_dal.get_data(body.user_id):
            action = google_oauth_dal.update_data

        data = await action(
            user_id=body.user_id,
            project_id=body.project_id,
            private_key=body.private_key,
            private_key_id=body.private_key_id,
            client_email=body.client_email,
            client_id=body.client_id,
            auth_uri=body.auth_uri,
            token_uri=body.token_uri,
            auth_provider_x509_cert_url=body.auth_provider_x509_cert_url,
            client_x509_cert_url=body.client_x509_cert_url,
            universe_domain=body.client_x509_cert_url,
        )

        return ShowGoogleOAuthResponse(
            id=data.id
        )

async def delete_google_oauth_data(body: GoogleOAuthDelete, db: AsyncSession) -> Union[ShowGoogleOAuthResponse, None]:
    async with db.begin():
        google_oauth_dal = GoogleOAuthDAL(db)

        if not await google_oauth_dal.get_data(body.user_id):
            return None
        
        result = await google_oauth_dal.delete_data(body.user_id)

        if result:
            return ShowGoogleOAuthResponse(
                id=body.user_id
            )
        
        return None
