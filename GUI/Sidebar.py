from tkinter import Frame, Button
from typing import Callable

class Sidebar(Frame):
    def __init__(self, master, width=200, bg="#2c3e50"):
        super().__init__(master, width=width, bg=bg)
        self.pack_propagate(False)
        self.buttons = []
        
    def add_button(self, text: str, command: Callable, **kwargs):
        """add a button to the sidebar"""
        btn = Button(
            self,
            text=text,
            bg="#34495e",
            fg="white",
            bd=0,
            highlightthickness=0,
            relief="flat",
            command=command,
            **kwargs
        )
        btn.pack(fill="x", padx=5, pady=2)
        self.buttons.append(btn)
        return btn

    def set_active_button(self, index: int):
        """set active button by index"""
        for i, btn in enumerate(self.buttons):
            if i == index:
                btn.config(bg="#3498db")
            else:
                btn.config(bg="#34495e")
