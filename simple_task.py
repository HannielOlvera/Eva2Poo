from .base_task import BaseTask

class SimpleTask(BaseTask):
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
