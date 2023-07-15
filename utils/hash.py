from passlib.context import CryptContext


class Hash:
    """
    A class that provides methods to hash and verify passwords.
    """

    def  __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def bcrypt_pass(self, password: str) -> str:
        """
        Hashes the specified password using the bcrypt scheme.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def verify_password(
            self,
            plain_password: str,
            hashed_password: str
    ) -> bool:
        """
        Verifies whether the specified plain password matches the specified
        hashed password.

        Args:
            plain_password (str): The plain password to be verified.
            hashed_password (str): The hashed password to be verified against.

        Returns:
            bool: True if the plain password matches the hashed password,
            False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)
