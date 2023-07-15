from datetime import datetime

from beanie import Document
from pydantic import (
    Field,
    EmailStr
)

class User(Document):
    """
    A data model representing a user in the database.

    Attributes:
        username (EmailStr): The user's email address.
        password (str): The user's password, hashed for security.

    Settings:
        name (str): The name of the database collection for User documents.

    Methods:
        __str__() -> str:
            Returns a string representation of the User object.
        __repr__() -> str:
            Returns a string representation of the User object for debugging purposes.
    """
    username: EmailStr = Field(
        description="Email of the user",
        example="example@gmail.com"
    )
    password: str = Field(
        description="Password of the user",
        example="$2b$12$OVZbIYJqsiyP.5NUOdrNUOLFC7l08dpN5DC7lG8VhP4A.nK/NI7Cy"
    )

    created: datetime = Field(
        default=datetime.now(),
        description="User creation time"
    )

    class Settings:
        name = "user_db"

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"<user: {self.username}>"
