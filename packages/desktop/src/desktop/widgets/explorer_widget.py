import customtkinter as ctk
from ttkbootstrap_icons_lucide import LucideIcon


class ExplorerWidget(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, label_text="Files", height=350, **kwargs)

        self.icon_file = LucideIcon("file-text", size=16, color="#FFFFFF").image
        self.icon_folder = LucideIcon("folder", size=16, color="#FFFFFF").image

        mock_files = [
            "server.properties",
            "eula.txt",
            "bukkit.yml",
            "spigot.yml",
            "plugins/",
            "world/",
            "logs/",
        ]
        for file_name in mock_files:
            icon = self.icon_folder if file_name.endswith("/") else self.icon_file
            btn = ctk.CTkButton(
                self,
                text=file_name,
                image=icon,
                fg_color="transparent",
                anchor="w",
            )
            btn.pack(fill="x", pady=2)
