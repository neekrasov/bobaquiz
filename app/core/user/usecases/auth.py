import uuid
from datetime import datetime, timedelta
from typing import Dict, Final

from jose import jwt
from passlib.context import CryptContext
from pydantic import SecretStr, ValidationError

from app.core.user.dto import (
    UserCreate,
    PairTokens,
    MetaJWT,
    UserJWT,
)
from app.core.user.protocols.dao import AuthDAO
from app.core.user.usecases.read_users import UserReaderService
from app.core.user.exceptions.user import UserAlreadyExists
from app.core.user.exceptions.auth import (
    TokenDoesNotExist,
    IncorrectUserCredentials,
    TokenDecodeError,
)
from app.core.user.entities.user import (
    HashedPassword,
    RawPassword,
    UserEntity,
    Username,
    Email,
)


class AuthUserService:
    jwt_token_type: Final = "Bearer"
    jwt_subject: Final = "access"
    algorithm: Final = "HS256"
    pwd_context: Final = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(
        self,
        auth_dao: AuthDAO,
        users_reader_service: UserReaderService,
        secret_key: SecretStr,
        access_token_expire: timedelta,
        refresh_token_expire: timedelta,
    ):
        self._users_reader_service = users_reader_service
        self._auth_dao = auth_dao
        self._access_token_expire = access_token_expire
        self._refresh_token_expire = refresh_token_expire
        self._secret_key = secret_key

    async def prepare_user_data_to_create(
        self,
        username: Username,
        password: RawPassword,
        email: Email,
        policy: bool,
    ) -> UserCreate:
        user = await self._users_reader_service.find_user_by_email(email=email)
        if user is not None:
            raise UserAlreadyExists

        return UserCreate(
            username=username,
            hashed_password=self._get_password_hash(password),
            email=email,
            policy=policy,
        )

    async def update_access_token(self, refresh_token: str) -> PairTokens:
        try:
            refresh_payload = self._decode_token(
                token=refresh_token,
                secret_key=self._secret_key.get_secret_value(),
            )
        except ValueError:
            raise TokenDecodeError

        user_id = refresh_payload["user_id"]
        session_id = refresh_payload["session_id"]

        user = await self._users_reader_service.find_user_by_id(
            user_id=user_id  # type: ignore
        )
        if user is None:
            raise IncorrectUserCredentials

        try:
            await self._auth_dao.delete_token_if_exists(session_id)
        except TokenDoesNotExist:
            raise IncorrectUserCredentials

        new_refresh_token = await self._create_refresh_token(
            user_id=user_id, session_id=str(uuid.uuid4())
        )
        new_access_token = self._create_access_token(email=user.email)

        return PairTokens(
            access_token=new_access_token, refresh_token=new_refresh_token
        )

    async def create_new_valid_pair(
        self, email: Email, raw_password: RawPassword
    ) -> PairTokens:
        user = await self._check_user_credentials(email, raw_password)

        if user is None:
            raise IncorrectUserCredentials

        access_token = self._create_access_token(email)
        refresh_token = await self._create_refresh_token(
            user_id=str(user.id), session_id=str(uuid.uuid4())
        )
        return PairTokens(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def delete_refresh_token(self, refresh_token: str) -> None:
        try:
            session_id = self._decode_token(
                refresh_token, self._secret_key.get_secret_value()
            )["session_id"]
        except ValueError:
            raise TokenDecodeError

        try:
            await self._auth_dao.delete_token_if_exists(session_id)
        except TokenDoesNotExist:
            raise IncorrectUserCredentials

    async def find_user_by_access_token(self, token: str) -> UserEntity | None:
        try:
            token_payload = self._decode_token(
                token, self._secret_key.get_secret_value()
            )
            user_jwt = UserJWT.parse_obj(token_payload)
        except (ValueError, ValidationError):
            raise TokenDecodeError

        return await self._users_reader_service.find_user_by_email(
            email=user_jwt.email
        )

    def _create_access_token(self, email: Email) -> str:
        token = self._create_jwt_token(
            jwt_content={"email": email},
            secret_key=self._secret_key.get_secret_value(),
            expires_delta=self._access_token_expire,
        )
        return token

    async def _create_refresh_token(
        self, session_id: str, user_id: str
    ) -> str:
        token = self._create_jwt_token(
            jwt_content={"session_id": session_id, "user_id": user_id},
            secret_key=self._secret_key.get_secret_value(),
            expires_delta=self._refresh_token_expire,
        )
        await self._auth_dao.save_refresh_token(
            token=token,
            session_id=session_id,
            refresh_token_expire=self._refresh_token_expire,
        )
        return token

    async def _check_user_credentials(
        self, email: Email, raw_password: RawPassword
    ) -> UserEntity | None:
        user = await self._users_reader_service.find_user_by_email(email=email)
        if user is None:
            return None

        if not self._verify_password(raw_password, user.hashed_password):
            return None
        return user

    def _create_jwt_token(
        self,
        *,
        jwt_content: Dict[str, str],
        secret_key: str,
        expires_delta: timedelta,
    ) -> str:
        to_encode = jwt_content.copy()
        to_encode.update(
            MetaJWT(
                exp=datetime.utcnow() + expires_delta,
                sub=self.jwt_subject,
            ).dict(),
        )
        token = jwt.encode(to_encode, secret_key, algorithm=self.algorithm)
        return token

    def _decode_token(self, token: str, secret_key: str) -> Dict[str, str]:
        try:
            return jwt.decode(token, secret_key, algorithms=[self.algorithm])
        except jwt.JWTError as decode_error:
            raise ValueError("unable to decode JWT token") from decode_error

    def _verify_password(
        self, raw_password: RawPassword, hashed_password: HashedPassword
    ) -> bool:
        return self.pwd_context.verify(raw_password, hashed_password)

    def _get_password_hash(self, password: RawPassword) -> HashedPassword:
        return HashedPassword(self.pwd_context.hash(str(password)))
