# src/app/views/task_list_item.py

import customtkinter as ctk
import tkinter as tk
from app.controllers.actions import TaskAction

class TaskListItem(ctk.CTkFrame):
    def __init__(self, master, task, action_callback, **kwargs):
        super().__init__(master, fg_color="#393d63", corner_radius=8, **kwargs)
        self.task = task
        self.action_callback = action_callback
        self._build_item()

    def _build_item(self):
        self.var = tk.BooleanVar(value=self.task.completed)
        self.checkbox = ctk.CTkCheckBox(self, variable=self.var, command=self._on_complete)
        self.checkbox.pack(side="left", padx=5, pady=5)

        self.label = ctk.CTkLabel(self, text=self.task.text, anchor="w")
        self.label.pack(side="left", fill="x", expand=True, padx=5)

        self.edit_btn = ctk.CTkButton(self, text="✎", width=30, command=self._on_edit)
        self.edit_btn.pack(side="right", padx=5)

        self.del_btn = ctk.CTkButton(self, text="🗑", width=30, command=self._on_delete)
        self.del_btn.pack(side="right", padx=5)

    def _on_complete(self):
        self.action_callback(TaskAction.COMPLETE, task_id=self.task.id)

    def _on_edit(self):
        self.action_callback(TaskAction.EDIT, task_id=self.task.id, text=None)

    def _on_delete(self):
        self.action_callback(TaskAction.DELETE, task_id=self.task.id)
