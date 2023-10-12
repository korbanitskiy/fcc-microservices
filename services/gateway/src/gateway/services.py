import typing

import gridfs
from pymongo import MongoClient

from gateway import clients, schemas


class GatewayService:
    def __init__(
        self,
        message_bus: clients.MessageBusClient,
        mongodb: MongoClient,
    ):
        self.message_bus = message_bus
        self.mongodb = mongodb

    def upload_video(self, user: schemas.User, video: typing.BinaryIO):
        fs = gridfs.GridFS(self.mongodb.videos)
        video_id = fs.put(video)
        try:
            self.notify_video_service(user, video_id)
        except Exception:
            fs.delete(video_id)
            raise

    def notify_video_service(self, user: schemas.User, video_id: str):
        self.message_bus.publish(
            queue="video", message={"video_id": video_id, "audio_id": None, "user": user.model_dump()}
        )

    def download_audio(self, audio_id: str):
        fs = gridfs.GridFS(self.mongodb.audios)
        audio = fs.get(audio_id)
        return audio
