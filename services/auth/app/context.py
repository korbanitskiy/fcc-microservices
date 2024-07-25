from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import models, services, settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_app_settings() -> settings.AppSettings:
    return settings.get_app_settings()


def get_user_service(settings: Annotated[settings.AppSettings, Depends(get_app_settings)]) -> services.UserService:
    return services.UserService(settings)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[services.UserService, Depends(get_user_service)],
) -> models.User:
    user = await user_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
