import logging
import time
import tkinter.messagebox as messagebox

from core.events import Signal, bus
from desktop.components.window_opener_mixin import WindowOpenerMixin
from desktop.windows.progress_window.progress_window import ProgressWindow


class InstanceSelectorActions(WindowOpenerMixin):
    def __init__(self, widget):
        self.widget = widget
        self.progress_windows = {}
        self._last_update_time = {}
        self._last_open_time = {}
        self.init_window_manager()

    def manage_server(self):
        if hasattr(self.widget, "_current_context_data"):
            self.open_server_window(self.widget._current_context_data)

    def on_double_click(self, data):
        bus.emit(Signal.CMD_CHECK_JAVA, server_data=data)

    def on_java_found(self, server_data):
        self.widget.after(50, lambda d=server_data: self.open_server_window(d))

    def on_java_not_found(self):
        self.widget.after(
            0,
            lambda: messagebox.showerror(
                "Java Not Found",
                "Java is not installed or not found on your system. Please install Java to continue.",
            ),
        )

    def open_server_window(self, data):
        server_id = data.get("id")
        now = time.time()
        last_open = self._last_open_time.get(server_id, 0)
        if now - last_open < 0.35:
            logging.info(
                f"[Desktop] InstanceSelectorActions: ignored rapid re-open for server_id={server_id}"
            )
            return

        logging.info(
            f"[Desktop] InstanceSelectorActions: opening ServerWindow for server_id={server_id}"
        )
        self._last_open_time[server_id] = now

        from desktop.windows import ServerWindow

        self.open_managed_window(
            ServerWindow,
            self.widget.winfo_toplevel(),
            window_key=data["id"],
            server_data=data,
        )

    def delete_server(self):
        if hasattr(self.widget, "_current_context_data"):
            server_name = self.widget._current_context_data.get("name", "Unknown")
            confirm = messagebox.askyesno(
                "Delete Server",
                f"Are you sure you want to completely DELETE '{server_name}'?\n\nThis will permanently erase all server files from your drive. This action CANNOT be undone.",
            )
            if confirm:
                bus.emit(
                    Signal.CMD_DELETE_SERVER,
                    server_id=self.widget._current_context_data["id"],
                )

    def remove_server(self):
        if hasattr(self.widget, "_current_context_data"):
            bus.emit(
                Signal.CMD_REMOVE_SERVER,
                server_id=self.widget._current_context_data["id"],
            )

    def open_folder(self):
        if hasattr(self.widget, "_current_context_data"):
            server_path = self.widget._current_context_data.get("path")
            if server_path:
                bus.emit(Signal.CMD_OPEN_FOLDER, path=server_path)

    def on_single_click(self, row_index, server_id):
        for i, frame in enumerate(self.widget.row_frames):
            frame.configure(
                fg_color=(
                    self.widget.selected_color
                    if i == row_index
                    else self.widget.default_color
                )
            )
        bus.emit(Signal.CMD_REQUEST_SERVER, server_id=server_id)

    def on_download_started(self, server_id, is_imported, server_name):
        def show():
            title = "Importing Server" if is_imported else "Downloading Server"
            text = (
                f"Importing '{server_name}' locally..."
                if is_imported
                else f"Downloading core for '{server_name}'..."
            )

            pw = ProgressWindow(
                self.widget.winfo_toplevel(),
                title=title,
                text=text,
                on_cancel=lambda: bus.emit(
                    Signal.CMD_CANCEL_DOWNLOAD, server_id=server_id
                ),
            )
            if is_imported:
                pw.set_indeterminate()
            self.progress_windows[server_id] = pw

        self.widget.after(0, show)

    def on_download_complete(self, server_id):
        def close_and_show():
            pw = self.progress_windows.pop(server_id, None)
            if pw:
                pw.close()
            messagebox.showinfo("Success", "Server added successfully!")
            bus.emit(Signal.CMD_REQUEST_ALL_SERVERS)

        self.widget.after(0, close_and_show)

    def on_download_error(self, server_id):
        def close_and_show():
            pw = self.progress_windows.pop(server_id, None)
            if pw:
                pw.close()
            messagebox.showerror(
                "Error", f"Failed to download core for server {server_id}."
            )

        self.widget.after(0, close_and_show)

    def on_download_progress(self, server_id, downloaded, total):
        current_time = time.time()
        last_time = self._last_update_time.get(server_id, 0)

        if current_time - last_time < 0.1 and downloaded < total:
            return

        self._last_update_time[server_id] = current_time

        def update():
            pw = self.progress_windows.get(server_id)
            if pw:
                mb_downloaded = downloaded / (1024 * 1024)
                if total > 0:
                    mb_total = total / (1024 * 1024)
                    pw.update_progress(
                        downloaded,
                        total,
                        f"Downloading... {mb_downloaded:.1f} MB / {mb_total:.1f} MB",
                    )
                else:
                    pw.set_indeterminate()
                    pw.update_progress(0, 0, f"Downloading... {mb_downloaded:.1f} MB")

        self.widget.after(0, update)
