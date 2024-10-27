from typing import List

from sqlalchemy import delete
from adapters.sqlalchemy_adapter.models.user import UserRolesTable
from core.entities.roles import UserRole
from core.protocols.roles import UserRoleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError


class UserRoleRepositoryImpl(UserRoleRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_role(self, role: UserRole) -> UserRole:
        pass

    async def delete_role(self, role_id: int):
        await self.session.execute(
            delete(UserRolesTable).where(UserRolesTable.id == role_id)
        )

    async def update_role(self, role_id: int) -> UserRole:
        pass

    async def get_all_roles(self, limit: int, offset: int) -> List[UserRole]:
        pass

    async def commit(self):
        try:
            await self.session.commit()
        except DBAPIError as error:
            await self.rollback()
            raise error

    async def rollback(self):
        await self.session.rollback()
