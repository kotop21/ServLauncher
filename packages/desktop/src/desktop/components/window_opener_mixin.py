import tkinter as tk
from typing import Dict, Type


class WindowOpenerMixin:
    def init_window_manager(self):
        self._opened_windows: Dict[str, tk.Toplevel] = {}

    def open_managed_window(
        self,
        window_class: Type,
        master: tk.Widget,
        window_key: str = "default",
        **kwargs,
    ):
        if not window_class:
            return None

        if (
            window_key not in self._opened_windows
            or not self._opened_windows[window_key].winfo_exists()
        ):
            main_app = master.winfo_toplevel()

            kwargs.pop("parent", None)
            kwargs.pop("master", None)

            win = window_class(main_app, **kwargs)
            self._opened_windows[window_key] = win
            print(f"[Desktop] Opened window: {window_class.__name__}")
        else:
            win = self._opened_windows[window_key]
            print(f"[Desktop] Focused existing window: {window_class.__name__}")

        def safe_topmost():
            try:
                if win.winfo_exists():
                    win.attributes("-topmost", False)
            except Exception:
                pass

        try:
            win.attributes("-topmost", True)
            win.after(100, safe_topmost)
        except Exception:
            pass

        win.focus()
        return win
