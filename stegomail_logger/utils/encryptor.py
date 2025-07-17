"""
Encryption utilities for payload protection in steganography.
Supports both XOR and AES encryption methods for educational purposes.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PayloadEncryptor:
    """
    Handles encryption and decryption of payloads using XOR or AES methods.
    """
    
    def __init__(self, method="xor", key="default_key"):
        """
        Initialize the encryptor with specified method and key.
        
        Args:
            method (str): Encryption method - 'xor' or 'aes'
            key (str): Encryption key
        """
        self.method = method.lower()
        self.key = key
        self.fernet = None
        
        if self.method == "aes":
            self._setup_aes()
    
    def _setup_aes(self):
        """
        Setup AES encryption using Fernet (AES 128 in CBC mode).
        """
        try:
            # Generate a key from the password
            password = self.key.encode()
            salt = b'salt_1234567890'  # In production, use random salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password))
            self.fernet = Fernet(key)
            logger.info("AES encryption initialized successfully")
        except Exception as e:
            logger.error(f"Failed to setup AES encryption: {e}")
            raise
    
    def xor_encrypt(self, data):
        """
        XOR encryption - simple educational cipher.
        
        Args:
            data (str): Data to encrypt
            
        Returns:
            str: Base64 encoded encrypted data
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            key_bytes = self.key.encode('utf-8')
            encrypted = bytearray()
            
            for i, byte in enumerate(data):
                encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            
            # Encode to base64 for safe storage in image
            encoded = base64.b64encode(bytes(encrypted)).decode('utf-8')
            logger.info("XOR encryption completed")
            return encoded
            
        except Exception as e:
            logger.error(f"XOR encryption failed: {e}")
            raise
    
    def xor_decrypt(self, encrypted_data):
        """
        XOR decryption - reverses XOR encryption.
        
        Args:
            encrypted_data (str): Base64 encoded encrypted data
            
        Returns:
            str: Decrypted data
        """
        try:
            # Decode from base64
            data = base64.b64decode(encrypted_data.encode('utf-8'))
            key_bytes = self.key.encode('utf-8')
            decrypted = bytearray()
            
            for i, byte in enumerate(data):
                decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
            
            result = bytes(decrypted).decode('utf-8')
            logger.info("XOR decryption completed")
            return result
            
        except Exception as e:
            logger.error(f"XOR decryption failed: {e}")
            raise
    
    def aes_encrypt(self, data):
        """
        AES encryption using Fernet.
        
        Args:
            data (str): Data to encrypt
            
        Returns:
            str: Base64 encoded encrypted data
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            encrypted = self.fernet.encrypt(data)
            encoded = base64.b64encode(encrypted).decode('utf-8')
            logger.info("AES encryption completed")
            return encoded
            
        except Exception as e:
            logger.error(f"AES encryption failed: {e}")
            raise
    
    def aes_decrypt(self, encrypted_data):
        """
        AES decryption using Fernet.
        
        Args:
            encrypted_data (str): Base64 encoded encrypted data
            
        Returns:
            str: Decrypted data
        """
        try:
            data = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.fernet.decrypt(data)
            result = decrypted.decode('utf-8')
            logger.info("AES decryption completed")
            return result
            
        except Exception as e:
            logger.error(f"AES decryption failed: {e}")
            raise
    
    def encrypt(self, data):
        """
        Encrypt data using the configured method.
        
        Args:
            data (str): Data to encrypt
            
        Returns:
            str: Encrypted data
        """
        if self.method == "xor":
            return self.xor_encrypt(data)
        elif self.method == "aes":
            return self.aes_encrypt(data)
        else:
            raise ValueError(f"Unsupported encryption method: {self.method}")
    
    def decrypt(self, encrypted_data):
        """
        Decrypt data using the configured method.
        
        Args:
            encrypted_data (str): Encrypted data
            
        Returns:
            str: Decrypted data
        """
        if self.method == "xor":
            return self.xor_decrypt(encrypted_data)
        elif self.method == "aes":
            return self.aes_decrypt(encrypted_data)
        else:
            raise ValueError(f"Unsupported decryption method: {self.method}")


def test_encryption():
    """
    Test function to demonstrate encryption functionality.
    """
    test_data = "print('Hello from encrypted payload!')"
    
    print("Testing XOR Encryption:")
    xor_encryptor = PayloadEncryptor("xor", "test_key_123")
    encrypted = xor_encryptor.encrypt(test_data)
    print(f"Encrypted: {encrypted[:50]}...")
    decrypted = xor_encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}\n")
    
    print("Testing AES Encryption:")
    aes_encryptor = PayloadEncryptor("aes", "test_key_123")
    encrypted = aes_encryptor.encrypt(test_data)
    print(f"Encrypted: {encrypted[:50]}...")
    decrypted = aes_encryptor.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    print(f"Match: {test_data == decrypted}")


if __name__ == "__main__":
    test_encryption()