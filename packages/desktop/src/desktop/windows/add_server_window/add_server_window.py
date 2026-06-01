import tkinter as tk
import customtkinter as ctk
from desktop.components import BaseWindow
from .add_server_actions import AddServerActions


class AddServerWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, title="Add Server", size=(500, 500))

        self._setup_ui()

        self.actions = AddServerActions(self)
        self.bind("<Destroy>", self.actions.on_destroy)

    def _get_theme_color(self, widget_type, property_name):
        color = ctk.ThemeManager.theme[widget_type][property_name]
        return self._apply_appearance_mode(color)

    def _create_listbox(self, parent):
        bg_color = self._get_theme_color("CTkFrame", "fg_color")
        text_color = self._get_theme_color("CTkLabel", "text_color")
        sel_bg = self._get_theme_color("CTkButton", "fg_color")

        container = ctk.CTkFrame(parent, fg_color="transparent")

        lb = tk.Listbox(
            container,
            bg=bg_color,
            fg=text_color,
            selectbackground=sel_bg,
            selectforeground="white",
            font=("TkDefaultFont", 13),
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
            exportselection=False,
        )

        scrollbar = ctk.CTkScrollbar(container, command=lb.yview)
        lb.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        lb.pack(side="left", expand=True, fill="both")

        return container, lb

    def _setup_ui(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.lbl_name = ctk.CTkLabel(self.container, text="Server Name:")
        self.lbl_name.pack(anchor="w")
        self.entry_name = ctk.CTkEntry(
            self.container, placeholder_text="My Awesome Server"
        )
        self.entry_name.pack(fill="x", pady=(0, 10))

        self.lbl_core = ctk.CTkLabel(self.container, text="Server Core (Engine):")
        self.lbl_core.pack(anchor="w")
        self.option_core = ctk.CTkOptionMenu(
            self.container,
            values=["Paper", "Purpur", "Import Local"],
        )
        self.option_core.pack(fill="x", pady=(0, 10))

        self.lists_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.lists_frame.pack(expand=True, fill="both", pady=(0, 10))

        self.version_container = ctk.CTkFrame(self.lists_frame, fg_color="transparent")
        self.version_container.pack(side="left", expand=True, fill="both", padx=(0, 5))

        self.lbl_version = ctk.CTkLabel(
            self.version_container, text="Minecraft Version:"
        )
        self.lbl_version.pack(anchor="w")

        self.entry_search_version = ctk.CTkEntry(
            self.version_container, placeholder_text="Search version..."
        )
        self.entry_search_version.pack(fill="x", pady=(0, 5))

        self.v_list_container, self.version_listbox = self._create_listbox(
            self.version_container
        )
        self.v_list_container.pack(expand=True, fill="both")

        self.build_container = ctk.CTkFrame(self.lists_frame, fg_color="transparent")
        self.build_container.pack(side="left", expand=True, fill="both", padx=(5, 0))

        self.lbl_build = ctk.CTkLabel(self.build_container, text="Core Build:")
        self.lbl_build.pack(anchor="w")

        self.entry_search_build = ctk.CTkEntry(
            self.build_container, placeholder_text="Search build..."
        )
        self.entry_search_build.pack(fill="x", pady=(0, 5))

        self.b_list_container, self.build_listbox = self._create_listbox(
            self.build_container
        )
        self.b_list_container.pack(expand=True, fill="both")

        self.btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.btn_frame.pack(fill="x", side="bottom", pady=(10, 0))

        self.btn_cancel = ctk.CTkButton(
            self.btn_frame,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
        )
        self.btn_cancel.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_confirm = ctk.CTkButton(self.btn_frame, text="Confirm")
        self.btn_confirm.pack(side="left", fill="x", expand=True, padx=(5, 0))
