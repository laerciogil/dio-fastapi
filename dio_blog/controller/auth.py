from fastapi import APIRouter

from dio_blog.security import sign_jwt
from dio_blog.schemas.auth import LoginRequest
from dio_blog.view.auth import LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    return sign_jwt(user_id = data.user_id)