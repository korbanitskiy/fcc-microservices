from gateway.settings import AppSettings
import httpx

class AuthService:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings