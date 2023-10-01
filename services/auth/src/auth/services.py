from datetime import datetime, timedelta
from typing import Optional

import ormar
from auth.models import User
from auth.settings import get_app_settings
from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_access_token(user: User, expires_delta: Optional[timedelta] = None) -> str:
    settings = get_app_settings()
    expires_delta = expires_delta or timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user.name,
        "exp": datetime.utcnow() + expires_delta,
    }
    return jwt.encode(payload, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)


async def find_active_user(name: str) -> Optional[User]:
    try:
        return await User.objects.get(name=name, disabled=False)
    except ormar.NoMatch:
        return None


async def authenticate_user(name: str, password: str) -> Optional[User]:
    user = await find_active_user(name)
    if not user:
        return None

    password_correct = verify_password(password, user.password)
    if not password_correct:
        return None

    return user


async def get_current_user(token: str) -> Optional[User]:
    settings = get_app_settings()
    try:
        payload = jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
        username = payload.get("sub", "")
    except JWTError:
        return None

    return await find_active_user(username)
