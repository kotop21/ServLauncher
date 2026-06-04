import tkinter as tk
import warnings
from typing import Any, Dict, List

import customtkinter as ctk
from core.events import Signal, bus
from desktop.components import SmartMenuButton
from ttkbootstrap_icons_lucide import LucideIcon

from .instance_selector_actions import InstanceSelectorActions

warnings.filterwarnings("ignore", category=UserWarning, module="customtkinter")


class ServerRowFrame(ctk.CTkFrame):
    _server_id: str
    _current_data: Dict[str, Any]
    _lbl_core: ctk.CTkLabel
    _lbl_port: ctk.CTkLabel


class InstanceSelectorWidget(ctk.CTkScrollableFrame):
    def __init__(self, master, status_bar=None, **kwargs):
        super().__init__(master, **kwargs)
        self.status_bar = status_bar
        self.grid_columnconfigure(0, weight=1)
        self.row_frames = []

        self.actions = InstanceSelectorActions(self)

        self.selected_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        self.default_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]

        self.server_icon = LucideIcon("server", size=20, color="#FFFFFF").image

        self.context_menu = tk.Menu(self, tearoff=0)
        self._build_context_menu()

        bus.subscribe(Signal.RESPONSE_ALL_SERVERS, self._on_servers_received)
        bus.subscribe(Signal.RESPONSE_SERVER, self._on_single_server_received)

        bus.subscribe(Signal.EVENT_DOWNLOAD_STARTED, self.actions.on_download_started)
        bus.subscribe(Signal.EVENT_DOWNLOAD_COMPLETE, self.actions.on_download_complete)
        bus.subscribe(Signal.EVENT_DOWNLOAD_ERROR, self.actions.on_download_error)
        bus.subscribe(Signal.EVENT_DOWNLOAD_PROGRESS, self.actions.on_download_progress)

        self.load_instances()

    def destroy(self):
        try:
            bus.unsubscribe(Signal.RESPONSE_ALL_SERVERS, self._on_servers_received)
            bus.unsubscribe(Signal.RESPONSE_SERVER, self._on_single_server_received)
            bus.unsubscribe(
                Signal.EVENT_DOWNLOAD_STARTED, self.actions.on_download_started
            )
            bus.unsubscribe(
                Signal.EVENT_DOWNLOAD_COMPLETE, self.actions.on_download_complete
            )
            bus.unsubscribe(Signal.EVENT_DOWNLOAD_ERROR, self.actions.on_download_error)
            bus.unsubscribe(
                Signal.EVENT_DOWNLOAD_PROGRESS, self.actions.on_download_progress
            )
        except Exception:
            pass
        super().destroy()

    def _build_context_menu(self):
        from desktop.windows import ServerWindow

        self.cmd_manage = SmartMenuButton(
            menu=self.context_menu,
            label="Manage server",
            master=self,
            window_class=ServerWindow,
            get_data=lambda: getattr(self, "_current_context_data", None),
        )

        self.context_menu.add_separator()
        self.context_menu.add_command(label="Folder", command=self.actions.open_folder)
        self.context_menu.add_command(
            label="Remove from list", command=self.actions.remove_server
        )
        self.context_menu.add_command(
            label="Delete permanently", command=self.actions.delete_server
        )

    def load_instances(self):
        bus.emit(Signal.CMD_REQUEST_ALL_SERVERS)

    def _on_servers_received(self, data: List[Dict]):
        if not self.winfo_exists():
            return

        if self.status_bar:
            self.status_bar.set_status("")

        current_ids = [getattr(f, "_server_id", None) for f in self.row_frames]
        new_ids = [d["id"] for d in data]

        if current_ids == new_ids:
            for i, instance in enumerate(data):
                frame = self.row_frames[i]
                frame._lbl_core.configure(
                    text=f"{instance['name']} ({instance['core']} {instance['version']})"
                )
                frame._lbl_port.configure(text=f"{instance['port']}")
                frame._current_data = instance
            return

        for frame in self.row_frames:
            try:
                frame.destroy()
            except Exception:
                pass
        self.row_frames.clear()

        for i, instance in enumerate(data):
            self._create_row(i, instance)

    def _create_row(self, row_index: int, data: Dict):
        row_frame = ServerRowFrame(self, fg_color=self.default_color, corner_radius=6)
        row_frame._server_id = data["id"]
        row_frame._current_data = data
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=2, padx=4)
        row_frame.grid_columnconfigure(1, weight=1)

        lbl_icon = ctk.CTkLabel(row_frame, text="", image=self.server_icon)  # type: ignore
        lbl_icon.grid(row=0, column=0, padx=(10, 5), pady=6)

        lbl_core = ctk.CTkLabel(
            row_frame,
            text=f"{data['name']} ({data['core']} {data['version']})",
            font=("", 14, "bold"),
        )
        lbl_core.grid(row=0, column=1, padx=5, pady=6, sticky="w")

        lbl_port = ctk.CTkLabel(row_frame, text=f"{data['port']}", text_color="gray60")
        lbl_port.grid(row=0, column=2, padx=10, pady=6, sticky="e")

        row_frame._lbl_core = lbl_core
        row_frame._lbl_port = lbl_port
        self.row_frames.append(row_frame)

        widgets = [row_frame, lbl_icon, lbl_core, lbl_port]
        for w in widgets:
            w.bind(
                "<Button-1>",
                lambda e, r=row_index, f=row_frame: self.actions.on_single_click(
                    r, f._current_data["id"]
                ),
            )
            w.bind(
                "<Double-Button-1>",
                lambda e, f=row_frame: self.actions.on_double_click(f._current_data),
            )
            w.bind(
                "<Button-3>",
                lambda e, r=row_index, f=row_frame: self._show_context_menu(
                    e, f._current_data, r
                ),
            )

    def _show_context_menu(self, event, data, row_index):
        self._current_context_data = data
        self.actions.on_single_click(row_index, data["id"])
        self.context_menu.post(event.x_root, event.y_root)

    def _on_single_server_received(self, data: Dict):
        if self.status_bar:
            hint_text = f"{data['name']} | {data['core']} {data['version']} | {data['port']} | {data['status']}"
            self.status_bar.set_status(hint_text)
