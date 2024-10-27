from dataclasses import dataclass

import bcrypt
from src.core.exception.exception import ItemDataConflict


@dataclass
class UserRole:
    service: str
    role: str

    @classmethod
    def create(cls, service: str, role: str):
        return cls(service=service, role=role)


@dataclass
class User:
    login: str
    email: str
    password_hash: str
    role: UserRole

    @classmethod
    def create(cls, login: str, email: str, password: str) -> "User":
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return cls(login=login, email=email, password_hash=password_hash)

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

