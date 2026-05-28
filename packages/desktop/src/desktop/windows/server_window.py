import customtkinter as ctk
from ttkbootstrap_icons_lucide import LucideIcon
from desktop.components import BaseWindow
from desktop.widgets import ConsoleWidget
from desktop.widgets import ExplorerWidget


class ServerWindow(BaseWindow):
    def __init__(self, server_data, **kwargs):
        super().__init__(title=server_data["name"], size=(950, 650), **kwargs)
        self.server_data = server_data

        self.resizable(True, True)
        self.minsize(550, 1)

        self._is_compact = False

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.header_frame = ctk.CTkFrame(self.main_scroll, corner_radius=8)
        self.header_frame.pack(fill="x", pady=(0, 15))

        self.lbl_name = ctk.CTkLabel(
            self.header_frame, text=self.server_data["name"], font=("", 24, "bold")
        )
        self.lbl_name.pack(side="left", padx=15, pady=15)

        info_text = f"{self.server_data['core']} {self.server_data['version']}  •  Port: {self.server_data['port']}  •  Status: {self.server_data['status']}"
        self.lbl_info = ctk.CTkLabel(
            self.header_frame, text=info_text, font=("", 14), text_color="gray50"
        )
        self.lbl_info.pack(side="left", padx=10, pady=15)

        self.middle_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.middle_frame.pack(fill="x", pady=(0, 15))

        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=0)
        self.middle_frame.grid_columnconfigure(2, weight=0, minsize=250)

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
        self.splitter.bind("<ButtonPress-1>", self._start_drag)
        self.splitter.bind("<B1-Motion>", self._on_drag)

        self.explorer_widget = ExplorerWidget(self.middle_frame, width=250)
        self.explorer_widget.grid(row=0, column=2, sticky="nsew")

        self.settings_header_frame = ctk.CTkFrame(
            self.main_scroll, fg_color="transparent"
        )
        self.settings_header_frame.pack(fill="x", pady=(10, 5), padx=5)

        self.lbl_settings = ctk.CTkLabel(
            self.settings_header_frame, text="Settings", font=("", 18, "bold")
        )
        self.lbl_settings.pack(side="left")

        self.settings_frame = ctk.CTkFrame(self.main_scroll, corner_radius=8)
        self.settings_frame.pack(fill="x", pady=(0, 20))

        self.lbl_java_args = ctk.CTkLabel(self.settings_frame, text="Java Arguments")
        self.lbl_java_args.pack(anchor="w", padx=15, pady=(15, 0))

        self.entry_args = ctk.CTkTextbox(self.settings_frame, height=80)
        self.entry_args.pack(fill="x", padx=15, pady=(5, 15))
        self.entry_args.insert("1.0", "-Xmx4G -Xms1G")

        self.bind("<Configure>", self._on_resize)

    def _start_drag(self, event):
        self._drag_start_x = event.x_root
        self._start_explorer_width = self.explorer_widget.cget("width")

    def _on_drag(self, event):
        if self._is_compact:
            return

        delta = self._drag_start_x - event.x_root
        new_width = self._start_explorer_width + delta

        max_width = self.middle_frame.winfo_width() - 300
        new_width = max(150, min(new_width, max_width))

        self.middle_frame.grid_columnconfigure(2, minsize=new_width)
        self.explorer_widget.configure(width=new_width)

    def _on_resize(self, event):
        if event.widget != self:
            return

        width = self.winfo_width()
        if width < 100:
            return

        if width < 850 and not self._is_compact:
            self.splitter.grid_remove()
            self.explorer_widget.grid(
                row=1, column=0, sticky="nsew", padx=0, pady=(15, 0)
            )
            self.middle_frame.grid_columnconfigure(2, minsize=0)
            self._is_compact = True
        elif width >= 850 and self._is_compact:
            self.splitter.grid()
            self.explorer_widget.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
            self.middle_frame.grid_columnconfigure(
                2, minsize=self.explorer_widget.cget("width")
            )
            self._is_compact = False
