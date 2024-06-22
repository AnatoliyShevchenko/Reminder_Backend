# Pydantic
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int = Field(ge=0)
    telegram_id: int = Field(ge=0)
    timezone: int = Field(ge=-11, le=13)
    language: str = Field()
    username: str
    password: str


class UsersSchema(BaseModel):
    response: list[UserSchema]


class CreateUserSchema(BaseModel):
    telegram_id: int = Field(ge=0)
    language: str = Field()
    timezone: int = Field(ge=-11, le=13)


class CreateAdminSchema(BaseModel):
    telegram_id: int = Field(ge=0)
    timezone: int = Field(ge=-11, le=13)
    language: str = Field()
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=10, max_length=32)


class AuthsSchema(BaseModel):
    username: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=10, max_length=32)


class TokenSchema(BaseModel):
    access_token: str

    