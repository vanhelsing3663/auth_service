from dataclasses import asdict, dataclass
from typing import Optional
from core.entities.roles import UserRole
from src.core.entities.user import User
from core.protocols.user import UserRepository


class UserRoleService:
    repository: UserRepository

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, dto: "UserCreateDto"):
        user = User.create(
            login=dto.login,
            email=dto.email,
            password_hash=dto.password_hash,
            roles=dto.roles,
        )
        await self.repository.create_user(user)
        await self.repository.commit()
        return UserReadDto.from_user(user)

    async def update_user(self, dto: "UserUpdateDto"):
        user = await self.repository.get_by_id(dto.id)

        for key, value in asdict(dto).items():
            if value is not None:
                setattr(user, key, value)

        await self.repository.update_user(user)
        await self.repository.commit()

        return UserReadDto.from_user(user)

    async def delete_user(self, login: str):
        await self.repository.delete_user(login)
    

@dataclass(frozen=True)
class UserCreateDto:
    login: str
    email: str
    password_hash: str
    roles: Optional[list[UserRole]] = None


@dataclass(frozen=True)
class UserUpdateDto:
    id: int
    login: str
    email: str
    password_hash: str
    roles: Optional[list[UserRole]] = None


@dataclass(frozen=True)
class UserReadDto:
    id: int
    login: str
    email: str
    password_hash: str
    roles: Optional[list[UserRole]] = None

    @classmethod
    def from_user(cls, user: "User"):
        return cls(id=user.id, login=user.login, email=user.email, roles=user.roles)
