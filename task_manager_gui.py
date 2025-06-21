
# src/app/views/task_manager_gui.py
import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import List
from datetime import datetime
from app.controllers.user_controller import UserController
from app.controllers.actions import TaskAction
from app.controllers.task_controller import TaskController
from app.controllers.task_factory import TaskFactory
from app.models.simple_task import SimpleTask
from app.store import TaskStore
from app.views.task_card import TaskCard
from app.utils.widget_helpers import make_button, make_entry

class TaskManagerGUI(ctk.CTkFrame):
    """Vista principal scrollable para gestionar tareas con JSON y GUI avanzada."""

    def __init__(
        self,
        master,
        task_controller: TaskController,
        user_controller: UserController,
        on_logout: callable,
        **kwargs
    ) -> None:
        super().__init__(master, **kwargs)
        self.task_controller = task_controller
        self.user_controller = user_controller
        self.on_logout = on_logout
        self.tasks: List[SimpleTask] = []

        # Persistencia local
        self.store = TaskStore()
        initial = self.task_controller.get_entities()
        for t in initial:
            self.store._tasks.append(t.to_dict())
        self.store.subscribe(self._refresh)

        # Construir UI
        self._build()
        self._render()
        self._bind_shortcuts()
        self._refresh()

    def _build(self) -> None:
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="#393d63")
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="Gestor de Tareas", font=("Segoe UI", 24))
        self.btn_logout = make_button(self.header_frame, "Cerrar sesión", self.on_logout)

        # Input
        self.input_frame = ctk.CTkFrame(self)
        self.entry = make_entry(self.input_frame, "Nueva tarea…")
        self.btn_add = make_button(self.input_frame, "Agregar", self._add_task)

        # Scrollable list
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="#232946")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
        # Contenedor interior
        self.list_container = ctk.CTkFrame(self.scrollable_frame)
        self.list_container.pack(fill="both", expand=True)

        # Error label
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")

    def _render(self) -> None:
        # Header
        self.header_frame.pack(fill="x", pady=10, padx=10)
        self.lbl_title.pack(side="left")
        self.btn_logout.pack(side="right")

        # Input
        self.input_frame.pack(fill="x", padx=10, pady=(0,10))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.btn_add.pack(side="left")

        # Error label
        self.error_label.pack(pady=(0,10), padx=10)

    def _bind_shortcuts(self) -> None:
        self.master.bind('<Control-n>', lambda e: self.entry.focus())
        self.master.bind('<Delete>', lambda e: self._delete_selected())

    def _refresh(self) -> None:
        # Limpiar container
        for widget in self.list_container.winfo_children():
            widget.destroy()

        raw = list(self.store)
        self.tasks = [TaskFactory.create(d) for d in raw]

        # Mostrar todas las tareas en scrollable
        for idx, task in enumerate(self.tasks):
            card = TaskCard(self.list_container, task, self._handle_action)
            card.grid(row=idx, column=0, sticky="ew", pady=5, padx=5)
            self.list_container.grid_columnconfigure(0, weight=1)

    def _add_task(self) -> None:
        text = self.entry.get().strip()
        if not text:
            self.error_label.configure(text="Texto vacío")
            return
        new_task = {
            'id': max((t['id'] for t in self.store), default=0) + 1,
            'text': text,
            'completed': False,
            'last_modified_by': self.user_controller.current_user['username'],
            'last_modified_at': None,
            'created_at': None,
            'user_id': self.user_controller.current_user['id'],
            'type': 'simple'
        }
        self.store.add(new_task)
        self.entry.delete(0, 'end')
        self.error_label.configure(text="")

    def _handle_action(self, action: TaskAction, **kwargs) -> None:
        task_id = kwargs.get('task_id')
        if action == TaskAction.COMPLETE:
            task = self._find_task(task_id)
            new_completed = not task.completed
            self.store.update(
                task_id,
                completed=new_completed,
                last_modified_by=self.user_controller.current_user['username'],
                last_modified_at=datetime.now().isoformat()
            )
        elif action == TaskAction.EDIT:
            current_text = self._find_task(task_id).text
            text = simpledialog.askstring("Editar tarea", "Nuevo texto:", initialvalue=current_text)
            if text:
                self.store.update(
                    task_id,
                    text=text,
                    last_modified_by=self.user_controller.current_user['username'],
                    last_modified_at=datetime.now().isoformat()
                )
        elif action == TaskAction.DELETE:
            current_text = self._find_task(task_id).text
            confirm = messagebox.askyesno("Eliminar tarea", f"¿Eliminar '{current_text}'? ")
            if confirm:
                self.store.remove(task_id)

    def _delete_selected(self) -> None:
        pass

    def _find_task(self, task_id: int) -> SimpleTask:
        return next(t for t in self.tasks if t.id == task_id)
