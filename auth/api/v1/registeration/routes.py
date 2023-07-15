from fastapi import (
    APIRouter,
    status
)

from .schemas import (
    RegisterUser,
    RegisterUserOut
)
from auth.repository.bll import UserService

registration_router = APIRouter()


@registration_router.post(
        "/register",
        status_code=status.HTTP_201_CREATED,
        response_model=RegisterUserOut
)
async def register(user_data: RegisterUser) -> RegisterUserOut:
    """
    Registers a new user.

    Args:
        user_data (RegisterUser): The user's registration details.

    Returns:
        RegisterUserOut: The newly registered user's information.

    Raises:
        HTTPException: If the registration fails due to invalid input or other errors.
    """
    user_service = UserService()
    user =  await user_service.register_user(
        username=user_data.username,
        password1=user_data.password1,
        password2=user_data.password2
    )
    return user
