from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

from gateway import clients, context, schemas, services

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_client: Annotated[clients.AuthClient, Depends(context.get_auth_client)],
):
    return auth_client.login(form_data.username, form_data.password)


@router.post("/upload-video")
def upload_video(
    video: UploadFile,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_client: Annotated[clients.AuthClient, Depends(context.get_auth_client)],
    gateway_service: Annotated[services.GatewayService, Depends(context.get_gateway_service)],
):
    user = auth_client.get_user(token)
    if not user.is_admin:
        raise HTTPException(403, detail="Video uploading is available for admin only")

    gateway_service.upload_video(user, video.file)


@router.get("/download-audio/{audio_id}")
def download_audio(
    audio_id: str,
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_client: Annotated[clients.AuthClient, Depends(context.get_auth_client)],
    gateway_service: Annotated[services.GatewayService, Depends(context.get_gateway_service)],
):
    user = auth_client.get_user(token)
    audio_file = gateway_service.download_audio(audio_id)

    def _iteraudio():
        with open(audio_file, mode="rb") as f:
            yield from f

    return StreamingResponse(_iteraudio(), media_type="audio/mpeg")
