from sqlalchemy import ForeignKey, Integer, String
from adapters.sqlalchemy_adapter.repositories.base import Base
from core.entities.user import User
from src.adapters.config_database import TableName
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRolesTable(Base):
    __tablename__ = TableName.USER_ROLES

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    service: Mapped[str] = mapped_column(String(100), nullable=False)

    users = relationship("UserTable", back_populates="user_role")


class UserTable(Base):
    __tablename__ = TableName.USERS

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[int] = mapped_column(
        ForeignKey(f"{TableName.USER_ROLES}.id"), nullable=True
    )

    user_role = relationship("UserRolesTable", back_populates="users")

    async def create_from_domain_object(cls, user: User) -> "UserTable":
        return cls(
            id=user.id,
            login=user.login,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role if user.role else None,
        )
