from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash:
    """
    A class that provides methods to hash and verify passwords.
    """
    @staticmethod
    def bcrypt_pass(password: str) -> str:
        """
        Hashes the specified password using the bcrypt scheme.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(
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
        return pwd_context.verify(plain_password, hashed_password)
