from _typeshed import Incomplete
from dio_blog.schemas.auth import LoginRequest as LoginRequest
from dio_blog.security import sign_jwt as sign_jwt
from dio_blog.view.auth import LoginResponse as LoginResponse

router: Incomplete

async def login(data: LoginRequest): ...
