from typing import List

from .interface import IAuthDataAccessLayer
from auth.models import User


class AuthDataAccessLayer(IAuthDataAccessLayer):
    """
    A data access layer for performing user-related operations on the database.
    """

    async def get_all_users(self) -> List[User]:
        """
        Returns a list of all users in the database.

        Returns:
            List[User]: A list of all users in the database.
        """
        return await User.find_all().to_list()

    async def get_user(self, username: str) -> User:
        """
        Returns the user with the provided username.

        Args:
            username (str): The username of the user to be returned.

        Returns:
            User: The user with the provided username.
        """
        return await User.find_one(User.username == username)

    async def create_user(self, username, password) -> User:
        """
        Creates a new user with the provided username and password.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly created user.
        """
        user = User(username=username, password=password)
        return await user.insert()

    async def delete_user(self, user: User) -> bool:
        """
        Deletes the provided user from the database.

        Args:
            user (User): The user to be deleted.

        Returns:
            bool: True if the user was deleted successfully, False otherwise.
        """
        return await user.delete()

    async def update_user(self, user: User, fields: dict) -> User:
        """
        Updates the provided user with the provided fields.

        Args:
            user (User): The user to be updated.
            fields (dict): A dictionary of fields to update.

        Returns:
            User: The updated user.
        """
        return await user.update({"$set": fields})
