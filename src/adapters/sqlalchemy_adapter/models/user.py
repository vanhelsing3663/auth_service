from sqlalchemy import ForeignKey, Integer, String
from adapters.sqlalchemy_adapter.repositories.base import Base
from core.entities.user import User
from src.adapters.config_database import TableName
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.adapters.sqlalchemy_adapter.models.roles import UserRolesTable


class UserTable(Base):
    __tablename__ = TableName.USERS

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    roles: Mapped[int] = mapped_column(
        ForeignKey(f"{TableName.USER_ROLES}.id"), nullable=True
    )

    user_role: Mapped["UserRolesTable"] = relationship(back_populates="users")

    async def create_from_domain_object(cls, user: User) -> "UserTable":
        return cls(
            id=user.id,
            login=user.login,
            email=user.email,
            password_hash=user.password_hash,
            role=user.roles if user.roles else None,
        )

    async def as_domain_object(self):
        return User(id=self.id, login=self.login, email=self.email, roles=self.roles)
