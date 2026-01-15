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
    RONEHA_DEV_KEY = (
        b'gAAAAABpaSKzi3z9M7b34iNDxcorLbqIM4CPoZ9-7a8oRpsPPyOUp9V9_ryz73YtFxetZnSCeN-45aLRCAMCZ0BuSPFaMBi1KOXC8b9IYEoc_7ugqf08F8s='
    )
    _SECRET_KEY = settings.SECRET_KEY

    @classmethod
    def get_base_path_academy(cls):
        crypto = CryptoManager(cls._SECRET_KEY)
        return crypto.decrypt(cls.RONEHA_DEV_KEY)
