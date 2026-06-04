from pathlib import Path

from core.events import Signal, bus


class ExplorerActions:
    def __init__(self, widget):
        self.widget = widget
        self.editable_extensions = {
            ".json",
            ".yml",
            ".yaml",
            ".properties",
            ".txt",
            ".xml",
            ".conf",
        }

    def request_directory(self, path):
        bus.emit(Signal.CMD_REQUEST_DIRECTORY, path=str(path))

    def check_for_updates(self):
        if hasattr(self.widget, "current_path") and hasattr(self.widget, "_last_mtime"):
            bus.emit(
                Signal.CMD_CHECK_DIRECTORY_UPDATE,
                path=str(self.widget.current_path),
                last_mtime=self.widget._last_mtime,
            )

    def enter_directory(self, path):
        self.widget.current_path = Path(path)
        self.request_directory(self.widget.current_path)

    def go_back(self):
        if self.widget.current_path != self.widget.server_path:
            parent = self.widget.current_path.parent
            self.widget.current_path = parent
            self.request_directory(parent)

    def open_file(self, path):
        bus.emit(Signal.CMD_READ_FILE, path=str(path), server_id=self.widget.server_id)

    def on_directory_received(self, path: str, items: list, mtime: float):
        if str(self.widget.current_path) == path:
            self.widget._last_mtime = mtime
            self.widget.render_items(items)
            self._update_top_bar(Path(path))

    def _update_top_bar(self, path):
        if path == self.widget.server_path:
            self.widget.lbl_path.configure(text="/")
            self.widget.btn_back.configure(state="disabled")
        else:
            rel_path = path.relative_to(self.widget.server_path)
            self.widget.lbl_path.configure(text=f"/{rel_path}")
            self.widget.btn_back.configure(state="normal")
