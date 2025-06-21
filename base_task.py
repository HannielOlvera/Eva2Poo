from abc import ABC, abstractmethod
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional

class BaseTask(ABC):
    def __init__(
        self,
        id: int,
        text: str,
        completed: bool,
        last_modified_by: str,
        last_modified_at: Optional[str],
        created_at: str,
        user_id: int
    ):
        self.id = id
        self.text = text
        self.completed = completed
        self.last_modified_by = last_modified_by
        # Parseamos fechas, permitiendo None o cadena vacía
        self.last_modified_at = self._parse_date(last_modified_at)
        self.created_at = self._parse_date(created_at)
        self.user_id = user_id

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """
        Intenta convertir date_str a datetime. Si es None o cadena vacía,
        devolvemos None; si falla parsedate_to_datetime, probamos ISO.
        """
        if not date_str:
            return None
        # Primero RFC-2822
        try:
            return parsedate_to_datetime(date_str)
        except Exception:
            pass
        # Luego ISO 8601
        try:
            return datetime.fromisoformat(date_str)
        except Exception:
            return None

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def display_text(self) -> str:
        pass
