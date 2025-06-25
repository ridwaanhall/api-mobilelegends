"""
Encryption utilities for MLBB project.
Author: ridwaanhall
"""

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class URLEncryption:
    """URL encryption/decryption utility class."""
    
    def __init__(self, key_string: str):
        """
        Initialize encryption with a key string.
        
        Args:
            key_string (str): The encryption key string
        """
        self.key_string = key_string
        self._fernet = self._create_fernet_key()
    
    def _create_fernet_key(self) -> Fernet:
        """Create a Fernet encryption key from the key string."""
        # Create a salt from the key string
        salt = hashlib.sha256(self.key_string.encode()).digest()[:16]
        
        # Derive a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.key_string.encode()))
        return Fernet(key)
    
    def encrypt_url(self, url: str) -> str:
        """
        Encrypt a URL string.
        
        Args:
            url (str): The URL to encrypt
            
        Returns:
            str: Base64 encoded encrypted URL
        """
        encrypted_data = self._fernet.encrypt(url.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()
    
    def decrypt_url(self, encrypted_url: str) -> str:
        """
        Decrypt an encrypted URL string.
        
        Args:
            encrypted_url (str): The encrypted URL (base64 encoded)
            
        Returns:
            str: Decrypted URL
        """
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_url.encode())
            decrypted_data = self._fernet.decrypt(encrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Failed to decrypt URL: {str(e)}")


def encrypt_mlbb_url(url: str, key: str = "IF_USE_THIS_INCLUDE_RIDWAANHALL_ON_YOUR_PROJECT") -> str:
    """
    Convenience function to encrypt MLBB URL.
    
    Args:
        url (str): The URL to encrypt
        key (str): The encryption key
        
    Returns:
        str: Encrypted URL
    """
    encryptor = URLEncryption(key)
    return encryptor.encrypt_url(url)


def decrypt_mlbb_url(encrypted_url: str, key: str = "IF_USE_THIS_INCLUDE_RIDWAANHALL_ON_YOUR_PROJECT") -> str:
    """
    Convenience function to decrypt MLBB URL.
    
    Args:
        encrypted_url (str): The encrypted URL
        key (str): The encryption key
        
    Returns:
        str: Decrypted URL
    """
    encryptor = URLEncryption(key)
    return encryptor.decrypt_url(encrypted_url)


def decrypt_url(encrypted_url: str = "Z0FBQUFBQm9XX0xIOWVvM2lpWm9hNDlsbE5Jd2ZDMHcxSHZvYVNRTUdqdjdLaTRIMnVTWi1MbFZfOUNadkNoaW15NU1zOERrU3RIbUlnRnhrSGRKRXNMWWNsQjVXTjBJeFdRQ1ZMMU5RWTBCWEk4cU92RHN6dXRlcnR2dkdnclNYaDN5cE5IXzdIQ2Y=", key: str = "IF_USE_THIS_INCLUDE_RIDWAANHALL_ON_YOUR_PROJECT") -> str:
    """
    Direct function to decrypt URL for use in settings.
    
    Args:
        encrypted_url (str): The encrypted URL
        key (str): The encryption key
        
    Returns:
        str: Decrypted URL
    """
    return decrypt_mlbb_url(encrypted_url, key)


def get_mlbb_url() -> str:
    """
    Get the decrypted MLBB URL.
    
    Returns:
        str: Decrypted MLBB URL
    """
    return decrypt_url()


# Alias for backward compatibility
encrypt_url = encrypt_mlbb_url
