from src.core.entities.user import UserRole
from typing import Protocol, List


class UserRoleRepository(Protocol):
    async def create_role(self, role: UserRole) -> UserRole:
        raise NotImplementedError

    async def delete_role(self, role_id: int):
        raise NotImplementedError

    async def update_role(self, role_id: int) -> UserRole:
        raise NotImplementedError

    async def get_all_roles(self, limit: int, offset: int) -> List[UserRole]:
        raise NotImplementedError
