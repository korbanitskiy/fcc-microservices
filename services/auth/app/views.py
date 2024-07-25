from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from app import context, models, schemas, services

login_router = APIRouter()
users_router = APIRouter(dependencies=[Depends(context.get_current_user)])


@login_router.get("/health-check")
async def health_check():
    return {"status": "ok"}


@login_router.post("/login", response_model=schemas.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[services.UserService, Depends(context.get_user_service)],
):
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_service.create_access_token(user)


@users_router.get("/users/me/", response_model=models.User)
async def get_users_me(user: Annotated[models.User, Depends(context.get_current_user)]):
    return user


@users_router.get("/users", response_model=list[models.User])
async def get_users_list(
    user_service: Annotated[services.UserService, Depends(context.get_user_service)],
) -> list[models.User]:
    return await user_service.get_active_users()
