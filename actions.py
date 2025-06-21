# src/app/controllers/actions.py

from enum import Enum, auto

class TaskAction(Enum):
    ADD = auto()
    EDIT = auto()
    DELETE = auto()
    COMPLETE = auto()
