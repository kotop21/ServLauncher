from typing import Callable, Optional, Type

import customtkinter as ctk

from .window_opener_mixin import WindowOpenerMixin


class SmartButton(ctk.CTkButton, WindowOpenerMixin):
    def __init__(
        self,
        master,
        status_bar=None,
        hover_text: str = "",
        window_class: Optional[Type] = None,
        window_kwargs: Optional[dict] = None,
        command: Optional[Callable] = None,
        **kwargs,
    ):
        self.init_window_manager()
        self.window_class = window_class
        self.window_kwargs = window_kwargs or {}

        def on_click():
            if self.window_class:
                self.open_managed_window(
                    self.window_class, master, **self.window_kwargs
                )
            if command:
                command()

        super().__init__(master, command=on_click, **kwargs)

        if status_bar and hover_text:
            self.bind("<Enter>", lambda e: status_bar.set_status(hover_text))
            self.bind("<Leave>", lambda e: status_bar.set_status(""))
