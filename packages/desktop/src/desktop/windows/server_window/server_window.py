import tkinter as tk

import customtkinter as ctk
from desktop.components import BaseWindow, SmartButton
from desktop.widgets.console.console_widget import ConsoleWidget
from desktop.widgets.explorer.explorer_widget import ExplorerWidget
from desktop.windows.server_settings.server_settings import ServerSettingsWindow
from ttkbootstrap_icons_lucide import LucideIcon

from .server_actions import ServerActions


class ServerWindow(BaseWindow):
    def __init__(self, master, server_data, **kwargs):
        server_id = server_data["id"]

        super().__init__(
            parent=master,
            title=server_data["name"],
            size=(950, 650),
            window_key=f"server_{server_id}",
            **kwargs,
        )

        self.server_data = server_data

        self.resizable(True, True)
        self.minsize(500, 300)

        self.actions = ServerActions(self)

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.header_frame = ctk.CTkFrame(self.main_frame, corner_radius=8)
        self.header_frame.pack(fill="x", pady=(0, 15))

        self.lbl_name = ctk.CTkLabel(
            self.header_frame, text=self.server_data["name"], font=("", 24, "bold")
        )
        self.lbl_name.pack(side="left", padx=15, pady=15)

        self.lbl_info = ctk.CTkLabel(
            self.header_frame, text="", font=("", 14), text_color="gray50"
        )
        self.lbl_info.pack(side="left", padx=10, pady=15)

        header_bg = self.header_frame.cget("fg_color")
        self.buttons_frame = ctk.CTkFrame(
            self.header_frame, fg_color=header_bg, corner_radius=8
        )
        self.buttons_frame.place(relx=1.0, rely=0.5, anchor="e", relheight=1.0)

        self.icon_settings = LucideIcon("settings", size=20, color="#FFFFFF").image
        self.btn_settings = SmartButton(
            master=self.buttons_frame,
            text="",
            image=self.icon_settings,
            width=40,
            height=40,
            fg_color="transparent",
            hover_text="Server settings",
            window_class=ServerSettingsWindow,
            window_kwargs={"server_data": self.server_data},
        )
        self.btn_settings.pack(side="right", padx=(5, 15), pady=10)

        self.icon_external = LucideIcon("external-link", size=20, color="#FFFFFF").image
        self.btn_open_external = ctk.CTkButton(
            self.buttons_frame,
            text="",
            image=self.icon_external,
            width=40,
            height=40,
            fg_color="transparent",
            command=self._show_external_folders_menu,
        )
        self.btn_open_external.pack(side="right", padx=(5, 0), pady=10)

        self.icon_folder = LucideIcon("folder", size=20, color="#FFFFFF").image
        self.btn_toggle_explorer = ctk.CTkButton(
            self.buttons_frame,
            text="",
            image=self.icon_folder,
            width=40,
            height=40,
            fg_color="transparent",
            command=self.actions.toggle_explorer,
        )
        self.btn_toggle_explorer.pack(side="right", padx=(10, 0), pady=10)

        self.middle_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.middle_frame.pack(fill="both", expand=True, pady=0)

        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=0)
        self.middle_frame.grid_columnconfigure(2, weight=0, minsize=250)
        self.middle_frame.grid_rowconfigure(0, weight=1)

        self.console_widget = ConsoleWidget(
            self.middle_frame, server_data=self.server_data
        )
        self.console_widget.grid(row=0, column=0, sticky="nsew")

        self.splitter = ctk.CTkFrame(
            self.middle_frame,
            width=8,
            cursor="sb_h_double_arrow",
            fg_color="transparent",
        )
        self.splitter.grid(row=0, column=1, sticky="ns", padx=2)

        self.splitter.bind(
            "<Enter>", lambda e: self.splitter.configure(fg_color=("gray70", "gray25"))
        )
        self.splitter.bind(
            "<Leave>", lambda e: self.splitter.configure(fg_color="transparent")
        )
        self.splitter.bind("<ButtonPress-1>", self.actions.start_drag)
        self.splitter.bind("<B1-Motion>", self.actions.on_drag)

        self.explorer_widget = ExplorerWidget(
            self.middle_frame,
            server_path=self.server_data["path"],
            server_id=self.server_data["id"],
            width=250,
        )
        self.explorer_widget.pack_propagate(False)
        self.explorer_widget.grid(row=0, column=2, sticky="nsew")

        self.actions.apply_saved_state()

        self.actions.setup_bus()
        self.actions.update_ui_state(self.server_data["status"])

        if hasattr(self.console_widget, "btn_kill"):
            self.console_widget.btn_kill.configure(command=self.actions.action_kill)

    def update_name_color(self, is_running: bool):
        color = "#4ade80" if is_running else ("gray10", "#DCE4EE")
        if self.lbl_name.winfo_exists():
            self.lbl_name.configure(text_color=color)

    def _show_external_folders_menu(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(
            label="Root directory",
            command=lambda: self.actions.open_in_system_explorer(),
        )
        menu.add_command(
            label="plugins",
            command=lambda: self.actions.open_in_system_explorer("plugins"),
        )
        menu.add_command(
            label="config",
            command=lambda: self.actions.open_in_system_explorer("config"),
        )
        menu.add_command(
            label="logs", command=lambda: self.actions.open_in_system_explorer("logs")
        )
        menu.add_command(
            label="crash-reports",
            command=lambda: self.actions.open_in_system_explorer("crash-reports"),
        )

        x = self.btn_open_external.winfo_rootx()
        y = self.btn_open_external.winfo_rooty() + self.btn_open_external.winfo_height()
        menu.post(x, y)

    def destroy(self):
        if hasattr(self, "actions"):
            self.actions.save_state()
            self.actions.cleanup_bus()

        super().destroy()
