from dataclasses import dataclass
from typing import Optional
import bcrypt
from src.core.exception.exception import ItemDataConflict


@dataclass
class UserRole:
    id: int
    service: str
    role: str

    @classmethod
    def create(cls, service: str, role: str):
        return cls(service=service, role=role)


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
