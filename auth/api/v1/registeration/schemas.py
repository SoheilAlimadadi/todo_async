from string import ascii_letters, digits, punctuation, ascii_uppercase, ascii_lowercase

from pydantic import (
    BaseModel,
    EmailStr,
    validator
)


class BaseRegisterUser(BaseModel):
    username: EmailStr
    password1: str
    password2: str


class RegisterUser(BaseRegisterUser):
    """
    A data model representing a user's registration details.

    Inherits from:
        BaseRegisterUser

    Attributes:
        password1 (str): The user's password.
        password2 (str): The user's password confirmation.

    Raises:
        ValueError: If the input values fail to meet the password validation criteria.
    """
    @validator('password1', 'password2')
    def validate_password(cls, password):
        """
        Validates the user's password based on the following criteria:
            - minimum length of 8 characters
            - at least one letter
            - at least one digit
            - at least one special character
            - at least one uppercase letter
            - at least one lowercase letter

        Args:
            password (str): The user's password to be validated.

        Raises:
            ValueError: If the password fails to meet any of the validation criteria.

        Returns:
            str: The validated password.
        """
        errors = []

        if len(password) < 8:
            errors.append('Password should have atleast 8 charaters.')

        if not any(map(lambda x: x in ascii_letters, password)):
            errors.append('Password should contain atleast one alphabet letter.')

        if not any(map(lambda x: x in digits, password)):
            errors.append('Password should contain atleast one digit.')

        if not any(map(lambda x: x in punctuation, password)):
            errors.append('Password should contain atleast one special character.')

        if not any(map(lambda x: x in ascii_uppercase, password)):
            errors.append('Password should contain atleast one uppercase letter.')

        if not any(map(lambda x: x in ascii_lowercase, password)):
            errors.append('Password should contain atleast one lowercase letter.')

        if errors:
            raise ValueError(", ".join(errors))

        return password

class RegisterUserOut(BaseModel):
    """
    A data model representing a registered user's information.

    Attributes:
        username (EmailStr): The registered user's email address.
    """
    username: EmailStr
