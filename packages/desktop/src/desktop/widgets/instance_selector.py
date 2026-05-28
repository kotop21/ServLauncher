import warnings
import tkinter as tk
import customtkinter as ctk
from typing import Dict
from ttkbootstrap_icons_lucide import LucideIcon
from desktop.components import SmartMenuButton

warnings.filterwarnings("ignore", category=UserWarning, module="customtkinter")


class InstanceSelector(ctk.CTkScrollableFrame):
    def __init__(self, master, status_bar=None, **kwargs):
        super().__init__(master, **kwargs)
        self.status_bar = status_bar
        self.grid_columnconfigure(0, weight=1)
        self.row_frames = []

        self.selected_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        self.default_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]

        self.server_icon = LucideIcon("server", size=20, color="#FFFFFF").image

        self.context_menu = tk.Menu(self, tearoff=0)
        self._build_context_menu()

        self.load_instances()

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
        self.context_menu.add_command(label="Start", command=self._action_start)
        self.context_menu.add_command(label="Stop", command=self._action_stop)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Folder")
        self.context_menu.add_command(label="Delete")

    def load_instances(self):
        data = self._get_mock_instances()
        for i, instance in enumerate(data):
            self._create_row(i, instance)

    def _create_row(self, row_index: int, data: Dict):
        row_frame = ctk.CTkFrame(self, fg_color=self.default_color, corner_radius=6)
        row_frame.grid(row=row_index, column=0, sticky="ew", pady=2, padx=4)

        row_frame.grid_columnconfigure(1, weight=1)

        lbl_icon = ctk.CTkLabel(row_frame, text="", image=self.server_icon)
        lbl_icon.grid(row=0, column=0, padx=(10, 5), pady=6)

        lbl_core = ctk.CTkLabel(
            row_frame,
            text=f"{data['name']} ({data['core']} {data['version']})",
            font=("", 14, "bold"),
        )
        lbl_core.grid(row=0, column=1, padx=5, pady=6, sticky="w")

        lbl_port = ctk.CTkLabel(row_frame, text=f"{data['port']}", text_color="gray60")
        lbl_port.grid(row=0, column=2, padx=10, pady=6, sticky="e")

        self.row_frames.append(row_frame)

        widgets = [row_frame, lbl_icon, lbl_core, lbl_port]
        hint_text = f"{data['name']} | {data['core']} {data['version']} | {data['port']} | {data['status']}"

        for w in widgets:
            w.bind(
                "<Button-1>",
                lambda e, r=row_index, txt=hint_text: self._on_single_click(r, txt),
            )
            w.bind("<Double-Button-1>", lambda e, d=data: self._on_double_click(d))
            w.bind(
                "<Button-3>",
                lambda e, d=data, r=row_index, txt=hint_text: self._show_context_menu(
                    e, d, r, txt
                ),
            )

    def _show_context_menu(self, event, data, row_index, text):
        self._current_context_data = data
        self._on_single_click(row_index, text)
        self.context_menu.entryconfigure(
            "Start", state="normal" if data["status"] != "Running" else "disabled"
        )
        self.context_menu.entryconfigure(
            "Stop", state="normal" if data["status"] == "Running" else "disabled"
        )
        self.context_menu.post(event.x_root, event.y_root)

    def _action_start(self):
        if hasattr(self, "_current_context_data"):
            print(
                f"[LOG] Start action triggered for {self._current_context_data['name']}"
            )

    def _action_stop(self):
        if hasattr(self, "_current_context_data"):
            print(
                f"[LOG] Stop action triggered for {self._current_context_data['name']}"
            )

    def _on_single_click(self, row_index, text):
        if self.status_bar:
            self.status_bar.set_status(text)
        for i, frame in enumerate(self.row_frames):
            frame.configure(
                fg_color=self.selected_color if i == row_index else self.default_color
            )

    def _on_double_click(self, data):
        self._current_context_data = data
        self.cmd_manage._on_click()

    def _get_mock_instances(self):
        return [
            {
                "id": 1,
                "name": "Main Survival",
                "core": "Paper",
                "version": "1.20.4",
                "status": "Running",
                "port": 25565,
            },
            {
                "id": 2,
                "name": "Lobby",
                "core": "Purpur",
                "version": "1.19.4",
                "status": "Stopped",
                "port": 25566,
            },
            {
                "id": 3,
                "name": "Minigames",
                "core": "Spigot",
                "version": "1.8.8",
                "status": "Waiting",
                "port": 25567,
            },
            {
                "id": 4,
                "name": "Anarchy",
                "core": "Folia",
                "version": "1.20.4",
                "status": "Stopped",
                "port": 25568,
            },
        ]

    def refresh_instances(self):
        for frame in self.row_frames:
            frame.destroy()
        self.row_frames = []
        self.load_instances()
