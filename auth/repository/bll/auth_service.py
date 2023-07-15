import logging

from fastapi import (
    HTTPException,
    status
)

from utils.hash import Hash
from auth.models import User
from auth.repository.dal import IAuthDataAccessLayer
from auth.exceptions import credentials_exception


coreLogger = logging.getLogger('core')


class UserService:
    """
    A service class for performing user-related operations.
    """
    @classmethod
    async def register_user(
            cls,
            dal: IAuthDataAccessLayer,
            username: str,
            password1: str,
            password2:str
    ) -> User:
        """
        Registers a new user with the provided username and passwords.

        Args:
            dal (ITaskDataAccessLayer): data access layer of user model
            username (str): The username of the new user.
            password1 (str): The user's password.
            password2 (str): The user's password confirmation.

        Returns:
            User: The newly created user.

        Raises:
            HTTPException: If the username is already in use or if
            the passwords do not match.
        """
        user = await dal.get_user(username)
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
        hashed_password = Hash.bcrypt_pass(password1)
        coreLogger.info(f"User: {username}, was registered")
        return await dal.create_user(username, hashed_password)

    @classmethod
    async def verify_credentials(
        cls,
        dal: IAuthDataAccessLayer,
        username: str,
        password: str
    ) -> User:
        """
        Verifies the provided username and password and returns the
        corresponding user.

        Args:
            dal (ITaskDataAccessLayer): data access layer of user model
            username (str): The username to be verified.
            password (str): The password to be verified.

        Returns:
            User: The user associated with the provided username and password.

        Raises:
            HTTPException: If the username or password is invalid.
        """
        user = await dal.get_user(username)
        if not user:
            coreLogger.error(
                f"Login attempt with a non-existant user, username: {username}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials, "
                "user with the provided username does not exist"
            )
        if not Hash.verify_password(password, user.password):
            coreLogger.error(
                f"Login attempt with wrong password, username: {username}"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials, invalid password"
            )
        coreLogger.info(f"user: {username} has logged-in")
        return user

    @classmethod
    async def get_user(
            cls,
            dal: IAuthDataAccessLayer,
            username: str,
    ) -> User:
        """
        Checks if user exists if it doesn't raises credentials error

        Args:
            dal (ITaskDataAccessLayer): data access layer of user model
            username (str): The username(email) of the user

        Returns:
            User: The user associated with the provided username

        Raises:
            credential_exception: If the username doesn't exist
        """
        user = await dal.get_user(username)
        if user is None:
            coreLogger.error(
                    "Credential error while verifying access token"
                    f"user: {username}, user does not exist."
                )
            raise credentials_exception
        return user
