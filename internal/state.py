from uuid import uuid4
from typing import Dict, Optional

class SessionManager:
    """
    Простой менеджер сессий в памяти.
    Хранит соответствие: токен (str) -> user_id (int).
    """
    def __init__(self):
        self.active_sessions: Dict[str, int] = {}

    def create_session(self, user_id: int) -> str:
        token = str(uuid4())
        self.active_sessions[token] = user_id
        return token

    def get_user_id(self, token: str) -> Optional[int]:
        if not token:
            return None
        return self.active_sessions.get(token)

    def remove_session(self, token: str):
        if token in self.active_sessions:
            del self.active_sessions[token]

# Глобальный экземпляр менеджера сессий
session_manager = SessionManager()
