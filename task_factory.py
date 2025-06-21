from typing import Dict, Any
from app.models.simple_task import SimpleTask
from app.models.task import Task

class TaskFactory:
    """Factory para crear instancias de tareas según su tipo."""

    @staticmethod
    def create(data: Dict[str, Any]) -> Task:
        # Hacemos copy para no mutar el dict original
        data_copy = data.copy()
        # Extraemos (y descartamos) la clave "type"
        ttype = data_copy.pop('type', 'simple')

        if ttype == 'simple':
            return SimpleTask(**data_copy)
        # Aquí podrías manejar otros tipos en el futuro
        return SimpleTask(**data_copy)
