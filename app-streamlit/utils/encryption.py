"""
암호화 및 복호화 유틸리티
"""

import os
from cryptography.fernet import Fernet

def _load_fernet() -> Fernet:
    """
    환경 변수에서 암호화 키를 로드하고, 없으면 새 키를 생성하여 반환
    """
    key_str = os.getenv("ENCRYPTION_ACCESS_KEY")
    if not key_str:
        new_key = Fernet.generate_key()
        print(f"생성된 암호화 키: {new_key.decode()}")
        key_bytes = new_key
    else:
        key_bytes = key_str.encode()
    return Fernet(key_bytes)

def encrypt_message(plain_text: str) -> str:
    """
    주어진 문자열을 암호화하여 URL-safe base64 문자열로 반환
    """
    f = _load_fernet()
    token = f.encrypt(plain_text.encode())
    return token.decode()

def decrypt_message(token: str) -> str:
    """
    암호화된 토큰을 복호화하여 원본 문자열 반환
    """
    f = _load_fernet()
    decrypted = f.decrypt(token.encode())
    return decrypted.decode()