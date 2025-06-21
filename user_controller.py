from typing import Optional, Dict
from app.api_client import APIClient
from app.controllers.base_controller import BaseController

class UserController(BaseController):
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.current_user: Optional[Dict] = None

    def _validate_credentials(self, username: str, password: str):
        if not username or not password:
            raise ValueError("Usuario y contraseña son obligatorios")

    def login(self, username: str, password: str) -> Dict:
        self._validate_credentials(username, password)
        result = self._handle_request(self.api_client.login, username, password)
        if result.get("success") and result.get("user_id"):
            self.current_user = {"id": result["user_id"], "username": result["username"]}
        return result

    def register(self, username: str, password: str) -> Dict:
        self._validate_credentials(username, password)
        return self._handle_request(self.api_client.register, username, password)

    def logout(self) -> None:
        self.current_user = None