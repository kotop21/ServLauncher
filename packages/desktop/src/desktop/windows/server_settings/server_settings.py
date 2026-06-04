import customtkinter as ctk

from .server_settings_actions import ServerSettingsActions


class ServerSettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, server_data, **kwargs):
        super().__init__(parent, **kwargs)
        self.server_data = server_data
        self.actions = ServerSettingsActions(self)

        self.title(f"Settings - {server_data['name']}")
        self.geometry("450x250")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.lbl_java_args = ctk.CTkLabel(
            self, text="Java Arguments", font=("", 14, "bold")
        )
        self.lbl_java_args.pack(anchor="w", padx=15, pady=(15, 5))

        self.entry_args = ctk.CTkTextbox(self, height=80)
        self.entry_args.pack(fill="x", padx=15, pady=(0, 15))

        saved_args = self.server_data.get("java_args", "-Xmx4G -Xms1G")
        self.entry_args.insert("1.0", saved_args)

        self.btn_save = ctk.CTkButton(self, text="Save", command=self.actions.save_args)
        self.btn_save.pack(pady=(0, 15))
