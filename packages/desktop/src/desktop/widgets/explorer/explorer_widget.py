from pathlib import Path

import customtkinter as ctk
from core.events import Signal, bus
from ttkbootstrap_icons_lucide import LucideIcon

from .explorer_actions import ExplorerActions


class ExplorerWidget(ctk.CTkFrame):
    def __init__(self, master, server_path, server_id=None, **kwargs):
        default_bg = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"]
        super().__init__(master, fg_color=default_bg, corner_radius=8, **kwargs)

        self.server_path = Path(server_path)
        self.current_path = self.server_path
        self.server_id = server_id
        self._last_mtime = 0
        self.actions = ExplorerActions(self)

        self.icon_file = LucideIcon("file-text", size=16, color="#FFFFFF").image
        self.icon_folder = LucideIcon("folder", size=16, color="#FFFFFF").image
        self.icon_back = LucideIcon("chevron-left", size=16, color="#FFFFFF").image

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent", height=40)
        self.top_bar.pack(fill="x", padx=10, pady=(10, 5))

        self.btn_back = ctk.CTkButton(
            self.top_bar,
            text="",
            image=self.icon_back,
            width=30,
            height=30,
            command=self.actions.go_back,
            state="disabled",
            fg_color="transparent",
        )
        self.btn_back.pack(side="left")

        self.lbl_path = ctk.CTkLabel(self.top_bar, text="/", font=("", 13, "bold"))
        self.lbl_path.pack(side="left", fill="x", expand=True, padx=10, anchor="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=(0, 10))

        bus.subscribe(Signal.RESPONSE_DIRECTORY, self.actions.on_directory_received)

        self.actions.request_directory(self.current_path)
        self._start_refresh_loop()

    def destroy(self):
        try:
            bus.unsubscribe(
                Signal.RESPONSE_DIRECTORY, self.actions.on_directory_received
            )
        except Exception:
            pass
        super().destroy()

    def _start_refresh_loop(self):
        if self.winfo_exists():
            self.actions.check_for_updates()
            self.after(1000, self._start_refresh_loop)

    def render_items(self, items):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for item in items:
            is_dir = item["is_dir"]
            name = item["name"]
            path = item["path"]

            icon = self.icon_folder if is_dir else self.icon_file

            cmd = None
            if is_dir:

                def dir_cmd(p=path):
                    self.actions.enter_directory(p)

                cmd = dir_cmd
            elif Path(path).suffix.lower() in self.actions.editable_extensions:

                def file_cmd(p=path):
                    self.actions.open_file(p)

                cmd = file_cmd

            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f" {name}",
                image=icon,
                fg_color="transparent",
                anchor="w",
                height=28,
                text_color="white" if is_dir else "gray70",
                command=cmd,
            )
            btn.pack(fill="x", pady=0)
