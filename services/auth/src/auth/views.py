from auth import models, schemas
from auth import services as svc
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/health-check")
async def health_check():
    return {"status": "ok"}


@router.post("/login", response_model=schemas.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await svc.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = svc.create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=models.User)
async def get_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await svc.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
