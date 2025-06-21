import customtkinter as ctk
from tkinter import messagebox
from app.controllers.user_controller import UserController
from app.views.base_view import BaseView

class LoginView(BaseView):
    def __init__(self, master, user_controller: UserController, on_login, on_register):
        self.user_controller = user_controller
        self.on_login = on_login
        self.on_register = on_register
        super().__init__(master)

    def build(self):
        self.header = ctk.CTkLabel(self, text="Iniciar Sesión", font=("Segoe UI", 24))
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.btn_login = ctk.CTkButton(self, text="Ingresar", command=self._do_login)
        self.btn_register = ctk.CTkButton(self, text="Registrar", command=self.on_register)

    def render(self):
        self.header.pack(pady=20)
        self.username_entry.pack(pady=10, padx=20, fill="x")
        self.password_entry.pack(pady=10, padx=20, fill="x")
        self.error_label.pack(pady=(5,15))
        self.btn_login.pack(pady=5)
        self.btn_register.pack(pady=5)

    def _do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        try:
            result = self.user_controller.login(username, password)
        except Exception as e:
            self.error_label.configure(text=str(e))
            return
        if result.get("success"):
            self.on_login()
        else:
            self.error_label.configure(text=result.get("error", "Credenciales inválidas"))