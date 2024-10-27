from dataclasses import dataclass
from typing import Optional
import bcrypt
from core.entities.roles import UserRole
from src.core.exception.exception import ItemDataConflict


@dataclass
class User:
    id: int
    login: str
    email: str
    password_hash: str
    role: Optional[UserRole] = None

    @classmethod
    def create(cls, login: str, email: str, password: str) -> "User":
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return cls(
            id=None,
            login=login,
            email=email,
            password_hash=password_hash,
            role=cls.role if cls.role else None,
        )

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
