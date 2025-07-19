import base64
import hashlib
from cryptography.fernet import Fernet
from django.conf import settings


class KeyDeriver:
    """Handles key derivation from a secret_key."""
    @staticmethod
    def derive_key(secret_key: str) -> bytes:
        key = hashlib.sha256(secret_key.encode()).digest()
        return base64.urlsafe_b64encode(key)

class CryptoManager:
    """Handles encryption and decryption using Fernet."""
    def __init__(self, secret_key: str):
        self.key = KeyDeriver.derive_key(secret_key)
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
