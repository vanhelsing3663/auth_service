from typing import Protocol, Optional, List
from src.core.entities.user import User
from src.core.entities.user import UserRole

class UserRepository(Protocol):
    async def create_user(self, login: str, email: str, password: str) -> User:
        """Создать пользователя с уникальным username и email."""
        raise NotImplementedError

    async def add_user_role(self, login: str, service: str, role: str) -> None:
        """Добавить роль пользователю для конкретного сервиса, если такой роли еще нет."""
        raise NotImplementedError

    async def delete_user(self, login: str) -> None:
        """Удалить пользователя по его username."""
        raise NotImplementedError

    async def get_all_users(self, page: int, limit: int) -> List[User]:
        """Получить список всех пользователей с пагинацией."""
        raise NotImplementedError

    async def get_user_by_credentials(self, login: str) -> Optional[User]:
        """Получить пользователя по логину."""
        raise NotImplementedError

    async def get_user_roles(self, login: str) -> List[UserRole]:
        """Получить роли пользователя по его имени."""
        raise NotImplementedError
    
    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError
