import customtkinter as ctk
from typing import Type, Optional, Callable


class SmartButton(ctk.CTkButton):
    def __init__(
        self,
        master,
        status_bar=None,
        hover_text: str = "",
        window_class: Optional[Type] = None,
        command: Optional[Callable] = None,
        **kwargs,
    ):
        self.window_class = window_class
        self.window_instance = None

        def on_click():
            if self.window_class:
                self._open_window()
            if command:
                command()

        super().__init__(master, command=on_click, **kwargs)

        if status_bar and hover_text:
            self.bind("<Enter>", lambda e: status_bar.set_status(hover_text))
            self.bind("<Leave>", lambda e: status_bar.set_status(""))

    def _open_window(self):
        if self.window_class is None:
            return

        if self.window_instance is None or not self.window_instance.winfo_exists():
            main_app = self.winfo_toplevel()
            self.window_instance = self.window_class(parent=main_app)
            self.window_instance.attributes("-topmost", True)
            self.window_instance.after(
                100, lambda: self.window_instance.attributes("-topmost", False)
            )

            self.window_instance.focus()
            print(f"[Desktop] Opened window: {self.window_class.__name__}")
        else:
            self.window_instance.attributes("-topmost", True)
            self.window_instance.after(
                100, lambda: self.window_instance.attributes("-topmost", False)
            )
            self.window_instance.focus()
            print(f"[Desktop] Focused existing window: {self.window_class.__name__}")
