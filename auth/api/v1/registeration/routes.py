from fastapi import (
    APIRouter,
    status,
    Depends
)

from .schemas import (
    RegisterUser,
    RegisterUserOut
)
from auth.repository.bll import UserService
from auth.repository.dal import (
    AuthDataAccessLayer,
    IAuthDataAccessLayer
)

registration_router = APIRouter()


@registration_router.post(
        "/register",
        status_code=status.HTTP_201_CREATED,
        response_model=RegisterUserOut
)
async def register(
    user_data: RegisterUser,
    dal: IAuthDataAccessLayer = Depends(AuthDataAccessLayer)
) -> RegisterUserOut:
    """
    Registers a new user.

    Args:
        user_data (RegisterUser): The user's registration details.

    Returns:
        RegisterUserOut: The newly registered user's information.

    Raises:
        HTTPException: If the registration fails due to invalid input or other errors.
    """
    user =  await UserService.register_user(
        dal=dal,
        username=user_data.username,
        password1=user_data.password1,
        password2=user_data.password2
    )
    return user
