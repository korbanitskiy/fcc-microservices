from datetime import datetime, timedelta
from typing import Optional

import ormar
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import models, schemas, settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


class UserService:
    def __init__(self, settings: settings.AppSettings) -> None:
        self.settings = settings

    def create_access_token(self, user: models.User, expires_minutes: int | None = None) -> schemas.Token:
        expires_minutes = expires_minutes or self.settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES
        payload = {
            "sub": user.name,
            "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
        }
        token = jwt.encode(payload, self.settings.auth.SECRET_KEY, algorithm=self.settings.auth.ALGORITHM)
        return schemas.Token(access_token=token, token_type="bearer")

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.settings.auth.SECRET_KEY, algorithms=[self.settings.auth.ALGORITHM])
        except JWTError:
            return {}

    async def find_active_user(self, name: str) -> models.User | None:
        try:
            return await models.User.objects.get(name=name, disabled=False)
        except ormar.NoMatch:
            return None

    async def authenticate_user(self, name: str, password: str) -> Optional[models.User]:
        user = await self.find_active_user(name)
        password_correct = user and verify_password(password, user.password)
        if password_correct:
            return user

        return None

    async def get_current_user(self, token: str) -> Optional[models.User]:
        payload = self.decode_access_token(token)
        username = payload.get("sub", "")
        return await self.find_active_user(username)

    async def get_active_users(self) -> list[models.User]:
        return await models.User.objects.all(disabled=False)
