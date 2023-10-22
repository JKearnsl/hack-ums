import uuid

from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime

from .role import RoleMedium, RoleSmall, Role
from src.models.state import UserState
from src.utils import validators


class User(BaseModel):
    """
    Модель пользователя

    """
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    bio: str | None
    role: Role
    state: UserState

    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class UserDocument(BaseModel):
    document_url: str | None


class UserMedium(BaseModel):
    """
    Модель пользователя

    """
    id: uuid.UUID
    email: EmailStr
    first_name: str
    last_name: str
    role: RoleMedium
    state: UserState

    created_at: datetime


class UserSmall(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    role: RoleSmall
    state: UserState

    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    bio: str = None

    @field_validator('password')
    def password_must_be_valid(cls, value):
        if not validators.is_valid_password(value):
            raise ValueError("Пароль должен быть валидным")
        return value

    @field_validator('first_name')
    def first_name_must_be_valid(cls, value):
        if value and not validators.is_valid_first_name(value):
            raise ValueError("Имя должно быть валидным")
        return value

    @field_validator('last_name')
    def last_name_must_be_valid(cls, value):
        if value and not validators.is_valid_last_name(value):
            raise ValueError("Фамилия должна быть валидной")
        return value


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    def password_must_be_valid(cls, value):
        if not validators.is_valid_password(value):
            raise ValueError("Пароль должен быть валидным")
        return value


class UserUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    bio: str = None

    @field_validator('first_name')
    def first_name_must_be_valid(cls, value):
        if value and not validators.is_valid_first_name(value):
            raise ValueError("Имя должно быть валидным")
        return value

    @field_validator('last_name')
    def last_name_must_be_valid(cls, value):
        if value and not validators.is_valid_last_name(value):
            raise ValueError("Фамилия должна быть валидной")
        return value

    @field_validator('bio')
    def bio_must_be_valid(cls, value):
        if value and len(value) > 255:
            raise ValueError("Биография должна быть не более 255 символов")
        return value


class UserUpdateByAdmin(UserUpdate):
    email: EmailStr = None
    role_id: uuid.UUID = None
    state: UserState = None
    bio: str = None
