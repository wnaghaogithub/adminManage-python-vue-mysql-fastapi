import hashlib
from datetime import datetime, timedelta

import jwt
from cryptography.fernet import Fernet

from .config import FERNET_KEY, JWT_ALGORITHM, JWT_EXPIRE_HOURS, JWT_SECRET

_fernet = Fernet(FERNET_KEY)


# ---------- 密码可逆加密（用户表，需展示明文）----------
def encrypt_password(plain: str) -> str:
    return _fernet.encrypt(plain.encode("utf-8")).decode("utf-8")


def decrypt_password(cipher: str) -> str:
    try:
        return _fernet.decrypt(cipher.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""


def mask_password(plain: str) -> str:
    """脱敏：保留前 2 位与后 1 位，中间打码"""
    if not plain:
        return ""
    if len(plain) <= 4:
        return "*" * len(plain)
    return f"{plain[:2]}****{plain[-1]}"


# ---------- 管理员密码单向哈希 ----------
def hash_password(plain: str) -> str:
    salt = "admin_manage_salt_v1"
    return hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt.encode("utf-8"), 100_000).hex()


def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed


# ---------- JWT ----------
def create_access_token(sub: str) -> str:
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
