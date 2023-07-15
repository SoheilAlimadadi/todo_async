from abc import ABC, abstractmethod
from typing import List

from auth.models import User


class IAuthDataAccessLayer(ABC):
    """
    An interface defining the user-related operations that can be performed on the database.

    Methods:
        get_all_users() -> List[User]:
            Returns a list of all users in the database.
        get_user(username: str) -> User:
            Returns the user with the provided username.
        create_user(username: str, password: str) -> User:
            Creates a new user with the provided username and password.
        delete_user(user: User) -> bool:
            Deletes the provided user from the database.
        update_user(user: User, fields: dict) -> User:
            Updates the provided user with the provided fields.
    """

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, username: str, password: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user: User) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User, fields: dict) -> User:
        raise NotImplementedError
