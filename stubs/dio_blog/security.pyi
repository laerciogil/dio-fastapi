from fastapi import Depends as Depends, Request as Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Annotated

SECRET_KEY: str
ALGORITHM: str
ACCESS_TOKEN_EXPIRE_SECONDS: int

class AccessToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str

class JWTToken(BaseModel):
    access_token: AccessToken

def sign_jwt(user_id: int) -> JWTToken: ...
async def decode_jwt(token: str) -> JWTToken | None: ...

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True) -> None: ...
    async def __call__(self, request: Request) -> JWTToken: ...

async def get_current_user(token: Annotated[JWTToken, None]) -> dict[str, int]: ...
def login_required(current_user: Annotated[dict[str, int], None]): ...
