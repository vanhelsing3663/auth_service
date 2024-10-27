from typing import List
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError
from adapters.sqlalchemy_adapter.models.user import UserTable
from core.entities.user import User
from core.protocols.user import UserRepository


class UserRepositoryImpl(UserRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, login: str, email: str, password: str):
        user = User.create(login=login, email=email, password=password)
        user_record = UserTable(
            login=user.login, email=user.email, password_hash=user.password_hash
        )

    async def delete_user(self, login: str) -> None:
        await self.session.execute(delete(UserTable).where(UserTable.login == login))

    async def get_all_users(self, page: int, limit: int) -> List[User]:
        pass

    async def add_user_role(self, login: str, service: str, role: str) -> None:
        user_role = User.add_role(login=login, service=service, role=role)

    async def commit(self):
        try:
            await self.session.commit()
        except DBAPIError as error:
            await self.rollback()
            raise error

    async def rollback(self):
        await self.session.rollback()
