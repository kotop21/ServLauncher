import logging
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
            win = None
            try:
                win = window_class(main_app, **kwargs)
                self._opened_windows[window_key] = win
                logging.info(f"[Desktop] Opened window: {window_class.__name__}")
            except Exception as e:
                logging.error(
                    f"[Desktop] Failed to open window {window_class.__name__}: {e}"
                )
                import traceback

                traceback.print_exc()
                if (
                    win is not None
                    and hasattr(win, "winfo_exists")
                    and win.winfo_exists()
                ):
                    try:
                        win.destroy()
                    except Exception:
                        pass
                self._opened_windows.pop(window_key, None)
                return None
        else:
            win = self._opened_windows[window_key]
            logging.info(f"[Desktop] Focused existing window: {window_class.__name__}")

        def safe_topmost():
            try:
                if win.winfo_exists():
                    win.attributes("-topmost", False)
            except Exception:
                pass

        try:
            if win.winfo_exists():
                win.deiconify()
                win.lift()
            win.attributes("-topmost", True)
            win.after(100, safe_topmost)
        except Exception:
            pass

        try:
            win.focus()
        except Exception:
            pass
        return win
