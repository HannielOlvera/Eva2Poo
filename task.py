from datetime import datetime
from email.utils import parsedate_to_datetime

class Task:
    def __init__(
        self,
        id: int,
        text: str,
        completed: bool,
        last_modified_by: str,
        last_modified_at: str,
        created_at: str,
        user_id: int
    ):
        # Validación de tipos
        if not isinstance(id, int) or not isinstance(user_id, int):
            raise TypeError("id y user_id deben ser enteros")
        if not isinstance(completed, bool):
            raise TypeError("completed debe ser booleano")

        self.id = id
        self.text = text
        self.completed = completed
        self.last_modified_by = last_modified_by

        # Parseo de fechas con parsedate_to_datetime (built-in)
        # parsedate_to_datetime entiende tanto RFC-2822 como ISO-8601
        self.last_modified_at = parsedate_to_datetime(last_modified_at) if last_modified_at else None
        try:
            self.created_at = parsedate_to_datetime(created_at)
        except Exception:
            # Fallback a fromisoformat si no es RFC-2822
            self.created_at = datetime.fromisoformat(created_at)

        self.user_id = user_id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "completed": self.completed,
            "last_modified_by": self.last_modified_by,
            "last_modified_at": self.last_modified_at.isoformat() if self.last_modified_at else None,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
        }

    def display_text(self) -> str:
        return f"{self.text}{' ✔' if self.completed else ''}"
