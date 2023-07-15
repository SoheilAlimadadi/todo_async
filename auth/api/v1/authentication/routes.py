from fastapi import (
    APIRouter,
    status,
    Depends
)

from fastapi.security import OAuth2PasswordRequestForm
from auth.repository.bll import UserService
from auth.repository.dal import (
    IAuthDataAccessLayer,
    AuthDataAccessLayer
)
from auth.authorization import (
    create_access_token,
    Token
)


authentication_router = APIRouter()


@authentication_router.post(
        "/login",
        status_code=status.HTTP_200_OK,
        response_model=Token
)
async def login(
    user_data: OAuth2PasswordRequestForm=Depends(),
    dal: IAuthDataAccessLayer = Depends(AuthDataAccessLayer)
) -> Token:
    """
    Authenticates a user and returns an access token.

    Args:
        user_data (OAuth2PasswordRequestForm): The user's login credentials.

    Returns:
        Token: An access token that can be used to access protected resources.

    Raises:
        HTTPException: If the user's login credentials are invalid.
    """
    user = await UserService.verify_credentials(
        dal=dal,
        username=user_data.username,
        password=user_data.password
    )
    access_token = create_access_token(data={"sub": user.username})
    return access_token
