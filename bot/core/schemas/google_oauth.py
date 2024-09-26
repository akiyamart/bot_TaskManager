from pydantic import BaseModel
from typing import Optional

class GoogleOAuthCreate(BaseModel):
    user_id: int
    project_id: str
    private_key_id: str
    private_key: str 
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str

class ShowGoogleOAuthResponse(BaseModel):  
    id: int

class GoogleOAuthDelete(BaseModel):
    user_id: int
