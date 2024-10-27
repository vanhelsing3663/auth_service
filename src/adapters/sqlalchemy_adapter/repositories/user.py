from typing import List
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from adapters.sqlalchemy_adapter.models.user import UserTable
from core.entities.user import User
from core.protocols.user import UserRepository


class UserRepositoryImpl(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User):
        user_record = UserTable.create_from_domain_object(user)
        await self.session.add(user_record)

    async def delete_user(self, login: str) -> None:
        await self.session.execute(delete(UserTable).where(UserTable.login == login))

    async def get_user_by_credentials(self, login: str):
        await self.session.execute(
            select(
                UserTable.id,
                UserTable.email,
                UserTable.login,
                UserTable.role,
            ).where(UserTable.login == login)
        )

    async def get_all_users(self, page: int, limit: int) -> List[User]:
        offset = (page - 1) * limit
        query = (
            select(
                UserTable.email,
                UserTable.login,
                UserTable.role,
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)
        users = result.fetchall()

    async def add_user_role(self, login: str, role: int) -> None:
        pass

    async def get_by_id(self, user_id: int):
        user_table = await self.session.get(UserTable, user_id)
        return user_table.as_domain_object()

    async def commit(self):
        try:
            await self.session.commit()
        except DBAPIError as error:
            await self.rollback()
            raise error

    async def rollback(self):
        await self.session.rollback()
