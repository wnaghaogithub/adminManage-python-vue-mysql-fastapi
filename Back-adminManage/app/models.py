from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    province: Mapped[str] = mapped_column(String(50), default="")
    city: Mapped[str] = mapped_column(String(50), default="")
    area: Mapped[str] = mapped_column(String(50), default="")
    avatar: Mapped[str] = mapped_column(String(255), default="")
    age: Mapped[int] = mapped_column(Integer, default=0)
    # 可逆加密存储，保证前端可切换展示明文
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Admin(Base):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    image: Mapped[str] = mapped_column(String(255), default="")  # 主题图片路径
    type: Mapped[str] = mapped_column(String(20), nullable=False)  # 厨艺 / 科学 / 编程
    content: Mapped[str] = mapped_column(Text, default="")  # wangEditor 富文本 HTML
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
