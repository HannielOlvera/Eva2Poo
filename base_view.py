import customtkinter as ctk
from abc import ABC, abstractmethod

class BaseView(ctk.CTkFrame, ABC):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#232946")
        self.pack(fill="both", expand=True)
        self.build()
        self.render()

    @abstractmethod
    def build(self):
        """Construye widgets básicos"""
        pass

    @abstractmethod
    def render(self):
        """Organiza layout y estilos finales"""
        pass

