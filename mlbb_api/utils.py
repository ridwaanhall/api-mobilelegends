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
    RIDWAANHALL_KEY = (
        b'gAAAAABoeT-lLhuQVXbSJl69DU2aaKr5yi1Ysm4bBfjB5ffkMSwBJWVUeylzU_yr9uo2z_Odsomt-Ya5X8eDrc9pbo1XP3LkZIE-fOG_Bql0Kuytth_S3d8='
    )
    _SECRET_KEY = settings.SECRET_KEY

    @classmethod
    def get_base_path(cls):
        crypto = CryptoManager(cls._SECRET_KEY)
        return crypto.decrypt(cls.RIDWAANHALL_KEY)
