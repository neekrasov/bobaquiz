from pydantic import BaseModel

from app.core.user.entities.user import (
    RawPassword,
    Username,
    Email,
)


class UserLoginFormRequest(BaseModel):
    username: Email  # auth by email
    password: RawPassword


class UserSignUpRequest(BaseModel):
    username: Username
    email: Email
    password: RawPassword
    policy: bool
