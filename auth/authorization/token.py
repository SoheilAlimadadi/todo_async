import logging
from typing import Annotated
from datetime import (
    timedelta,
    datetime
)

from jose import (
    jwt,
    JWTError
)
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from kernel.settings.auth import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from auth.models import User
from .schema import Token
from auth.exceptions import credentials_exception



coreLogger = logging.getLogger('core')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

def create_access_token(data: dict) -> Token:
    """
    Creates a new access token using the provided data.

    Args:
        data (dict): A dictionary containing the data to be encoded in the access token.

    Returns:
        Token: An access token object containing the encoded token and its type.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    token = Token(access_token=encoded_jwt, token_type="bearer")
    coreLogger.info(f"JWT access token was created for user: {data.get('sub')}")
    return token

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Verifies the provided access token and returns the corresponding user.

    Args:
        token (Annotated[str, Depends(oauth2_scheme)]): The access token to be verified.

    Returns:
        User: The user associated with the provided access token.

    Raises:
        credentials_exception: If the access token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            coreLogger.error(
                "Credential error while verifying access token"
                f"user: {username}"
            )
            raise credentials_exception
    except JWTError as e:
        coreLogger.error(
            "Credential error while verifying access token"
            f"user: {username}, error: {e}"
            )
        raise credentials_exception
    user = await get_user(username)
    return user

async def get_user(
        username: str,
) -> User:
    user = await User.find_one(User.username==username)
    if user is None:
        coreLogger.error(
                "Credential error while verifying access token"
                f"user: {username}, user does not exist."
            )
        raise credentials_exception
    return user
