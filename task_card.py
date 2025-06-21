import customtkinter as ctk
import tkinter as tk
from typing import Callable, Any
from app.controllers.actions import TaskAction
from app.utils.widget_helpers import make_button
from datetime import datetime

class TaskCard(ctk.CTkFrame):
    """Tarjeta reutilizable para mostrar y actuar sobre una tarea, con información de última modificación."""

    def __init__(self, master, task: Any, action_cb: Callable, **kwargs) -> None:
        super().__init__(master, fg_color="#393d63", corner_radius=8, **kwargs)
        self.task = task
        self.action_cb = action_cb
        self._build()

    def _build(self) -> None:
        # Checkbox sin texto
        self.var = tk.BooleanVar(value=self.task.completed)
        self.checkbox = ctk.CTkCheckBox(
            self,
            text="",
            variable=self.var,
            command=self._on_complete
        )
        self.checkbox.grid(row=0, column=0, padx=5, pady=5)

        # Texto principal de la tarea
        self.label = ctk.CTkLabel(
            self,
            text=self.task.text,
            anchor="w"
        )
        self.label.grid(row=0, column=1, sticky="ew", padx=5)

        # Botones de editar y eliminar
        self.edit_btn = make_button(self, "✎", self._on_edit)
        self.edit_btn.grid(row=0, column=2, padx=5)

        self.del_btn = make_button(self, "🗑", self._on_delete)
        self.del_btn.grid(row=0, column=3, padx=5)

        # Información de última modificación o creación
        info_text = self._format_info()
        self.info_label = ctk.CTkLabel(
            self,
            text=info_text,
            font=("Segoe UI", 10),
            text_color="#a0a0a0",
            anchor="w"
        )
        self.info_label.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=(0,5))

        self.grid_columnconfigure(1, weight=1)

    def _format_info(self) -> str:
        """Genera texto con quién y cuándo modificó o creó la tarea."""
        if self.task.last_modified_at:
            date = self._format_datetime(self.task.last_modified_at)
            user = self.task.last_modified_by or "Desconocido"
            return f"Modificado por {user} el {date}"
        elif self.task.created_at:
            date = self._format_datetime(self.task.created_at)
            user = getattr(self.task, 'created_by', self.task.last_modified_by) or "Desconocido"
            return f"Creado por {user} el {date}"
        return "Sin información de historial"

    @staticmethod
    def _format_datetime(dt: datetime) -> str:
        if not dt:
            return "Fecha desconocida"
        return dt.strftime("%Y-%m-%d %H:%M")

    def _on_complete(self) -> None:
        self._flash("#3fa34d")
        self.action_cb(
            TaskAction.COMPLETE,
            task_id=self.task.id,
            completed=self.var.get(),
            last_modified_by=self.task.last_modified_by
        )

    def _on_edit(self) -> None:
        self.action_cb(
            TaskAction.EDIT,
            task_id=self.task.id,
            text=None,
            last_modified_by=self.task.last_modified_by
        )

    def _on_delete(self) -> None:
        self.action_cb(
            TaskAction.DELETE,
            task_id=self.task.id
        )

    def _flash(self, color: str, duration: int = 200) -> None:
        orig = self.cget("fg_color")
        self.configure(fg_color=color)
        self.after(duration, lambda: self.configure(fg_color=orig))