import tkinter as tk
from typing import Type, Optional, Callable, Dict


class SmartMenuButton:
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
        self.window_class = window_class
        self.command = command
        self.master = master
        self.get_data = get_data
        self.opened_windows = {}

        menu.add_command(label=label, command=self._on_click, **kwargs)

    def _on_click(self):
        data = self.get_data() if self.get_data else None

        if self.window_class:
            self._open_window(data)
        if self.command:
            self.command()

    def _open_window(self, data: Optional[Dict]):
        if self.window_class is None:
            return

        window_key = data["id"] if data and "id" in data else "default"

        if (
            window_key not in self.opened_windows
            or not self.opened_windows[window_key].winfo_exists()
        ):
            main_app = self.master.winfo_toplevel()
            if data:
                self.opened_windows[window_key] = self.window_class(
                    server_data=data, parent=main_app
                )
            else:
                self.opened_windows[window_key] = self.window_class(parent=main_app)

            self.opened_windows[window_key].focus()
            print(f"[Desktop] Opened window: {self.window_class.__name__}")
        else:
            self.opened_windows[window_key].focus()
            print(f"[Desktop] Focused existing window: {self.window_class.__name__}")
