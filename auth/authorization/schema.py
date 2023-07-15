from pydantic import BaseModel


class Token(BaseModel):
    """
    A data model representing an access token.

    Attributes:
        access_token (str): The encoded access token.
        token_type (str): The type of the access token (e.g. "bearer").
    """
    access_token: str
    token_type: str
