from pathlib import Path

from core.app_config import config
from core.events import Signal, bus
from desktop.windows.editor.editor_window import EditorWindow


class ServerActions:
    def __init__(self, window):
        self.window = window
        self._drag_start_x = 0
        self._start_explorer_width = 0
        self._explorer_visible = True

    def apply_saved_state(self):
        server_id = self.window.server_data["id"]
        self._explorer_visible = config.get(
            f"server_{server_id}_explorer_visible", True
        )
        try:
            raw_width = config.get(f"server_{server_id}_explorer_width", 250)
            width = int(raw_width) if raw_width is not None else 250
        except (ValueError, TypeError):
            width = 250

        if not self._explorer_visible:
            self.window.explorer_widget.grid_remove()
            self.window.splitter.grid_remove()
            self.window.middle_frame.grid_columnconfigure(2, minsize=0)
        else:
            self.window.middle_frame.grid_columnconfigure(2, minsize=width)
            self.window.explorer_widget.configure(width=width)

    def save_state(self):
        server_id = self.window.server_data["id"]
        config.set(f"server_{server_id}_explorer_visible", self._explorer_visible)

        if self._explorer_visible:
            width = self.window.explorer_widget.cget("width")
            if isinstance(width, int):
                config.set(f"server_{server_id}_explorer_width", width)

    def setup_bus(self):
        bus.subscribe(Signal.SERVER_STATUS_CHANGED, self.on_status_changed)
        bus.subscribe(Signal.RESPONSE_FILE_CONTENT, self.on_file_content_received)

    def cleanup_bus(self):
        try:
            bus.unsubscribe(Signal.SERVER_STATUS_CHANGED, self.on_status_changed)
            bus.unsubscribe(Signal.RESPONSE_FILE_CONTENT, self.on_file_content_received)
        except Exception:
            pass

    def on_file_content_received(
        self, path: str, content: str, server_id: int, success: bool
    ):
        if server_id == self.window.server_data["id"] and success:
            EditorWindow(self.window, path, content, server_id)

    def toggle_explorer(self):
        if self._explorer_visible:
            self.window.explorer_widget.grid_remove()
            self.window.splitter.grid_remove()
            self.window.middle_frame.grid_columnconfigure(2, minsize=0)
            self._explorer_visible = False
        else:
            self.window.splitter.grid()
            self.window.explorer_widget.grid()
            server_id = self.window.server_data["id"]

            try:
                raw_width = config.get(f"server_{server_id}_explorer_width", 250)
                width = int(raw_width) if raw_width is not None else 250
            except (ValueError, TypeError):
                width = 250

            self.window.middle_frame.grid_columnconfigure(2, minsize=width)
            self.window.explorer_widget.configure(width=width)
            self._explorer_visible = True

    def open_in_system_explorer(self, subfolder: str = ""):
        target_path = Path(self.window.server_data["path"])
        if subfolder:
            target_path = target_path / subfolder
            try:
                target_path.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
        bus.emit(Signal.CMD_OPEN_FOLDER, path=str(target_path))

    def action_kill(self):
        bus.emit(Signal.CMD_KILL_SERVER, server_id=self.window.server_data["id"])

    def on_status_changed(self, server_id: int, new_status: str):
        if (
            not hasattr(self.window, "server_data")
            or server_id != self.window.server_data["id"]
        ):
            return
        self.window.server_data["status"] = new_status
        self.update_ui_state(new_status)

    def update_ui_state(self, status: str):
        if not self.window.winfo_exists():
            return
        info_text = f"{self.window.server_data['core']} {self.window.server_data['version']}  •  Port: {self.window.server_data['port']}  •  Status: {status}"
        self.window.lbl_info.configure(text=info_text)

        is_running = status == "Running"
        if hasattr(self.window.console_widget, "btn_start"):
            self.window.console_widget.btn_start.configure(
                state="disabled" if is_running else "normal"
            )
        if hasattr(self.window.console_widget, "btn_stop"):
            self.window.console_widget.btn_stop.configure(
                state="normal" if is_running else "disabled"
            )
        if hasattr(self.window.console_widget, "btn_kill"):
            self.window.console_widget.btn_kill.configure(
                state="normal" if is_running else "disabled"
            )

    def start_drag(self, event):
        self._drag_start_x = event.x_root
        self._start_explorer_width = self.window.explorer_widget.winfo_width()

    def on_drag(self, event):
        if not self._explorer_visible:
            return
        delta = self._drag_start_x - event.x_root
        new_width = self._start_explorer_width + delta
        max_width = self.window.middle_frame.winfo_width() - 300
        new_width = max(150, min(new_width, max_width))
        self.window.middle_frame.grid_columnconfigure(2, minsize=new_width)
        self.window.explorer_widget.configure(width=new_width)
