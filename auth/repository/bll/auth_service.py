import logging

from fastapi import (
    HTTPException,
    status,
    Depends
)

from utils.hash import Hash
from auth.models import User
from auth.repository.dal import AuthDataAccessLayer


coreLogger = logging.getLogger('core')


class UserService:

    def __init__(self):
        """
         A service class for performing user-related operations.
        """
        self.dal = AuthDataAccessLayer()

    async def register_user(
            self,
            username: str,
            password1: str,
            password2:str,
    ) -> User:
        """
        Registers a new user with the provided username and passwords.

        Args:
            username (str): The username of the new user.
            password1 (str): The user's password.
            password2 (str): The user's password confirmation.

        Returns:
            User: The newly created user.

        Raises:
            HTTPException: If the username is already in use or if the passwords do not match.
        """
        user = await self.dal.get_user(username)
        if user:
            coreLogger.error(
                f"User: {username} tried to register an existing user"
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="username already in use"
            )
        if not password1 == password2:
            coreLogger.error(f"User: {username}, entered unmacthed passes")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        password_hasher = Hash()
        hashed_password = password_hasher.bcrypt_pass(password1)
        coreLogger.info(f"User: {username}, was registered")
        return await self.dal.create_user(username, hashed_password)

    async def verify_credentials(self, username: str, password: str) -> User:
        """
        Verifies the provided username and password and returns the corresponding user.

        Args:
            username (str): The username to be verified.
            password (str): The password to be verified.

        Returns:
            User: The user associated with the provided username and password.

        Raises:
            HTTPException: If the username or password is invalid.
        """
        user = await self.dal.get_user(username)
        if not user:
            coreLogger.error(
                f"Login attempt with a non-existant user, username: {username}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials, "
                "user with the provided username does not exist"
            )
        password_hasher = Hash()
        if not password_hasher.verify_password(password, user.password):
            coreLogger.error(
                f"Login attempt with wrong password, username: {username}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials, invalid password"
            )
        coreLogger.info(f"user: {username} has logged-in")
        return user
