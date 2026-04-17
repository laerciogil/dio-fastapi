import time
import jwt

from typing import Annotated
from uuid import uuid4
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600

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

def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()
    payload = {
        "iss": "dio-blog",
        "sub": str(user_id),
        "aud": "dio-blog-users",
        "exp": now + ACCESS_TOKEN_EXPIRE_SECONDS,
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}

async def decode_jwt(token: str) -> JWTToken | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="dio-blog-users")
        _token = JWTToken.model_validate({"access_token": payload})
        return _token if _token.access_token.exp > time.time() else None
    except Exception:
        return None
    
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> JWTToken:
        if credentials:
            token = await decode_jwt(credentials.credentials)
            if token:
                return token
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")
    
async def get_current_user(token: Annotated[JWTToken, Depends(JWTBearer())]) -> dict[str, int]:
    print(token)
    return {"user_id": int(token.access_token.sub)}

def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied.")
    return current_user