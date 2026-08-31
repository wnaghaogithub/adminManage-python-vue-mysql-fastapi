from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    province: str = ""
    city: str = ""
    area: str = ""
    avatar: str = ""
    age: int = 0
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    province: str | None = None
    city: str | None = None
    area: str | None = None
    avatar: str | None = None
    age: int | None = None
    password: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    province: str
    city: str
    area: str
    avatar: str
    age: int
    password: str  # 明文，前端负责脱敏显示
    create_time: datetime


class PageOut(BaseModel):
    total: int
    items: list[UserOut]


class ArticleCreate(BaseModel):
    title: str
    image: str = ""
    type: str
    content: str = ""


class ArticleUpdate(BaseModel):
    title: str | None = None
    image: str | None = None
    type: str | None = None
    content: str | None = None


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    image: str
    type: str
    content: str
    create_time: datetime


class ArticlePageOut(BaseModel):
    total: int
    items: list[ArticleOut]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str
    username: str
