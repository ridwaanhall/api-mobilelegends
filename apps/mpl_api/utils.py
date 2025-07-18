import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings


class KeyDeriver:
    """Handles key derivation from a password."""
    @staticmethod
    def derive_key(password: str) -> bytes:
        key = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(key)


class CryptoManager:
    """Handles encryption and decryption using Fernet."""
    def __init__(self, password: str):
        self.key = KeyDeriver.derive_key(password)
        self.fernet = Fernet(self.key)

    def encrypt(self, text: str) -> bytes:
        return self.fernet.encrypt(text.encode())

    def decrypt(self, token: bytes) -> str:
        return self.fernet.decrypt(token).decode()


class BasePathProvider:
    """Provides the base path using encrypted key and secret."""
    MPL_ID_TOKEN = (
        b'gAAAAABoeo8Tdv0oDuR-f40iOHFSanbIWvq5qWnIK0mmUFjyd-8pXi2oYaSJdORsscKnmuDRVC6WesscOckUnDTp71nSwaRKF1nGVR_3Yuv0Hzk0mURN5Gw='
    )
    _SECRET_KEY = settings.SECRET_KEY

    @classmethod
    def get_mpl_id_path(cls):
        crypto = CryptoManager(cls._SECRET_KEY)
        return crypto.decrypt(cls.MPL_ID_TOKEN)
