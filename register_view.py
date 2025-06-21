import customtkinter as ctk
from tkinter import messagebox
from app.controllers.user_controller import UserController
from app.views.base_view import BaseView

class RegisterView(BaseView):
    def __init__(self, master, user_controller: UserController, on_register_success, on_cancel):
        self.user_controller = user_controller
        self.on_register_success = on_register_success
        self.on_cancel = on_cancel
        super().__init__(master)

    def build(self):
        self.header = ctk.CTkLabel(self, text="Registro", font=("Segoe UI", 24))
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.btn_register = ctk.CTkButton(self, text="Registrar", command=self._do_register)
        self.btn_cancel = ctk.CTkButton(self, text="Cancelar", command=self.on_cancel)

    def render(self):
        self.header.pack(pady=20)
        self.username_entry.pack(pady=10, padx=20, fill="x")
        self.password_entry.pack(pady=10, padx=20, fill="x")
        self.error_label.pack(pady=(5,15))
        self.btn_register.pack(pady=5)
        self.btn_cancel.pack(pady=5)

    def _do_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        try:
            result = self.user_controller.register(username, password)
        except Exception as e:
            self.error_label.configure(text=str(e))
            return
        if result.get("success"):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.on_register_success()
        else:
            self.error_label.configure(text=result.get("error", "Error al registrar"))