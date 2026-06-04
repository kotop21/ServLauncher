import tkinter as tk
from typing import Callable, Optional, Type

from .window_opener_mixin import WindowOpenerMixin


class SmartMenuButton(WindowOpenerMixin):
    def __init__(
        self,
        menu: tk.Menu,
        label: str,
        master: tk.Widget,
        window_class: Optional[Type] = None,
        command: Optional[Callable] = None,
        get_data: Optional[Callable] = None,
        **kwargs,
    ):
        self.init_window_manager()
        self.window_class = window_class
        self.command = command
        self.master = master
        self.get_data = get_data

        menu.add_command(label=label, command=self._on_click, **kwargs)

    def _on_click(self):
        data = self.get_data() if self.get_data else None

        if self.window_class:
            window_key = data["id"] if data and "id" in data else "default"
            win_kwargs = {"server_data": data} if data else {}

            self.open_managed_window(
                self.window_class, self.master, window_key=window_key, **win_kwargs
            )

        if self.command:
            self.command()
