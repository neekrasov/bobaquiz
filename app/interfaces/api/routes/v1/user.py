from fastapi import APIRouter, Depends, HTTPException, status

from app.shared import Mediator
from app.core.user.entities.user import UserEntity
from app.core.user.usecases.auth import AuthUserService
from app.core.user.usecases.create_user import CreateUserCommand
from app.core.user.dto import PairTokens
from app.core.user.exceptions.user import UserAlreadyExists
from app.core.user.exceptions.auth import (
    IncorrectUserCredentials,
    TokenDecodeError,
)
from ..request_models.user import UserSignUpRequest, UserLoginFormRequest
from ..response_models.user import UserReadResponse
from ...di.providers.auth import get_login_form
from ...di.stubs import (
    provide_auth_service_stub,
    provide_current_user_stub,
    provide_mediator_stub,
)


router = APIRouter(
    prefix="/users",
)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    new_user: UserSignUpRequest,
    auth_user_service: AuthUserService = Depends(provide_auth_service_stub),
    mediator: Mediator = Depends(provide_mediator_stub),
):
    if not new_user.policy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must accept the privacy policy",
        )
    try:
        prepared_data = await auth_user_service.prepare_user_data_to_create(
            username=new_user.username,
            password=new_user.password,
            email=new_user.email,
            policy=new_user.policy,
        )
        await mediator.send_command(CreateUserCommand(user=prepared_data))
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user already exists",
        )

    return {"message": "User created successfully"}


@router.post(
    "/login",
    summary="login",
    response_model=PairTokens,
)
async def login(
    form_data: UserLoginFormRequest = Depends(get_login_form),
    auth_user_service: AuthUserService = Depends(provide_auth_service_stub),
):
    try:
        token = await auth_user_service.create_new_valid_pair(
            email=form_data.username, raw_password=form_data.password
        )
    except IncorrectUserCredentials:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect login or password",
        )
    return token


@router.post(
    "/refresh-token",
    summary="Get new Pair Tokens",
    response_model=PairTokens,
)
async def get_new_refresh_token(
    refresh_token: str,
    auth_user_service: AuthUserService = Depends(provide_auth_service_stub),
):
    try:
        token = await auth_user_service.update_access_token(refresh_token)
    except (IncorrectUserCredentials, TokenDecodeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect credentials",
        )
    return token


@router.post(
    "/logout",
    summary="Logout",
    status_code=status.HTTP_200_OK,
)
async def logout(
    refresh_token: str,
    auth_user_service: AuthUserService = Depends(provide_auth_service_stub),
):
    try:
        await auth_user_service.delete_refresh_token(refresh_token)
    except (IncorrectUserCredentials, TokenDecodeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect credentials",
        )
    return {"message": "Successfully logged out"}


@router.get(
    "/me",
    summary="Get current user",
    response_model=UserReadResponse,
)
async def get_me(
    user: UserEntity = Depends(provide_current_user_stub),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="could not validate credentials",
        )

    user_dict = user.dict()
    user_dict.update({"subscription": user.subscription.type})
    return user_dict
