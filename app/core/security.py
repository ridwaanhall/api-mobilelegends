"""
Security Utilities Module

This module provides cryptographic functions for the application.
"""

import base64
import hashlib
from typing import Union

from cryptography.fernet import Fernet


class KeyDeriver:
    """Handles key derivation from a secret key."""
    
    @staticmethod
    def derive_key(secret_key: str) -> bytes:
        """
        Derive a Fernet-compatible key from a secret key.
        
        Args:
            secret_key: The secret key string
            
        Returns:
            bytes: Base64-encoded 32-byte key
        """
        key = hashlib.sha256(secret_key.encode()).digest()
        return base64.urlsafe_b64encode(key)


class CryptoManager:
    """Handles encryption and decryption using Fernet symmetric encryption."""
    
    def __init__(self, secret_key: str):
        """
        Initialize crypto manager.
        
        Args:
            secret_key: Secret key for encryption/decryption
        """
        self.key = KeyDeriver.derive_key(secret_key)
        self.fernet = Fernet(self.key)
    
    def encrypt(self, text: str) -> bytes:
        """
        Encrypt text.
        
        Args:
            text: Plain text to encrypt
            
        Returns:
            bytes: Encrypted token
        """
        return self.fernet.encrypt(text.encode())
    
    def decrypt(self, token: Union[bytes, str]) -> str:
        """
        Decrypt token.
        
        Args:
            token: Encrypted token (bytes or string)
            
        Returns:
            str: Decrypted text
            
        Raises:
            cryptography.fernet.InvalidToken: If decryption fails
        """
        if isinstance(token, str):
            token = token.encode()
        return self.fernet.decrypt(token).decode()


class BasePathProvider:
    """Provides the base path using encrypted key and secret."""
    
    # Encrypted base path token
    RONE_DEV_KEY = (
        b'gAAAAABoeVABaPKjWkRGpRV7c7bmRASNq4aZcN_cLGeeWU0OSNFtWLahn4mn9AYq4PqpkJKjA8rx4-Jk2oqjfLTB7l3u9tC_ufGi1x5IcdWrinV26tcdotw='
    )
    
    def __init__(self, secret_key: str):
        """
        Initialize base path provider.
        
        Args:
            secret_key: Secret key for decryption
        """
        self.crypto = CryptoManager(secret_key)
    
    def get_base_path(self) -> str:
        """
        Get decrypted base path.
        
        Returns:
            str: Decrypted base path
            
        Raises:
            cryptography.fernet.InvalidToken: If decryption fails
        """
        return self.crypto.decrypt(self.RONE_DEV_KEY)
