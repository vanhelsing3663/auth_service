from sqlalchemy import ForeignKey, Integer, String
from adapters.sqlalchemy_adapter.repositories.base import Base
from src.adapters.config_database import TableName
from sqlalchemy.orm import Mapped, mapped_column


class UserTable(Base):
    __tablename__ = TableName.USERS

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)


class UserRolesTable(Base):
    __tablename__ = TableName.USER_ROLES

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    service: Mapped[str] = mapped_column(String(100), nullable=False)
