"""JWT token creation and password hashing utilities."""
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import secrets
import string
import time

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, username: str, role: str) -> str:
    """Create short-lived JWT access token (15 min)."""
    now = int(time.time())
    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60),
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """Create a long-lived opaque refresh token (7 days)."""
    return secrets.token_urlsafe(64)


def decode_access_token(token: str) -> dict:
    """Decode and validate access token. Raises jwt.PyJWTError on failure."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


def generate_booking_reference() -> str:
    """Generate a unique booking reference: MOV-XXXXXX."""
    chars = string.ascii_uppercase + string.digits
    return "MOV-" + "".join(secrets.choice(chars) for _ in range(6))
