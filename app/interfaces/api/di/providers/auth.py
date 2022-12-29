from fastapi import Depends

from fastapi import HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from app.core.user.usecases.auth import AuthUserService
from app.core.user.entities.user import (
    RawPassword,
    UserEntity,
    Username,
)
from app.core.user.exceptions.auth import (
    TokenDecodeError,
)
from ...routes.request_models.user import UserLoginFormRequest
from ....api.di.stubs import provide_auth_service_stub

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
)


async def get_current_user(
    token: str = Depends(oauth2_schema),
    auth_service: AuthUserService = Depends(provide_auth_service_stub),
) -> UserEntity | None:
    try:
        user = await auth_service.find_user_by_access_token(token=token)
    except TokenDecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
        )
    return user


def get_login_form(
    user: OAuth2PasswordRequestForm = Depends(),
) -> UserLoginFormRequest:
    return UserLoginFormRequest(
        username=Username(user.username),
        password=RawPassword(user.password),
    )
