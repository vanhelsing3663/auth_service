from sqlalchemy import Integer, String
from adapters.sqlalchemy_adapter.repositories.base import Base
from src.adapters.config_database import TableName
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.adapters.sqlalchemy_adapter.models.user import UserTable


class UserRolesTable(Base):
    __tablename__ = TableName.USER_ROLES

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    service: Mapped[str] = mapped_column(String(100), nullable=False)

    users: Mapped["UserTable"] = relationship(back_populates="user_role")
