import customtkinter as ctk
from desktop.components import BaseWindow


class AddServerWindow(BaseWindow):
    def __init__(self, parent):
        super().__init__(parent, title="Add Server", size=(400, 300))

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=40, pady=40)

        self.entry_name = ctk.CTkEntry(self.container, placeholder_text="Server Name")
        self.entry_name.pack(fill="x", pady=10)

        self.option_core = ctk.CTkOptionMenu(
            self.container,
            values=[
                "Paper",
                "Purpur (Paper fork)",
                "Pufferfish (Paper fork)",
                "Velocity",
                "Folia",
            ],
        )
        self.option_core.pack(fill="x", pady=10)

        self.option_version = ctk.CTkOptionMenu(
            self.container, values=["1.20.4", "1.19.4", "1.8.8"]
        )
        self.option_version.pack(fill="x", pady=10)

        self.btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.btn_frame.pack(fill="x", pady=(20, 0))

        self.btn_cancel = ctk.CTkButton(
            self.btn_frame,
            text="Cancel",
            fg_color="transparent",
            border_width=1,
            command=self.destroy,
        )
        self.btn_cancel.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_confirm = ctk.CTkButton(
            self.btn_frame, text="Confirm", command=self._on_confirm
        )
        self.btn_confirm.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def _on_confirm(self):
        name = self.entry_name.get()
        core = self.option_core.get()
        version = self.option_version.get()
        print(f"Added server: {name} | {core} | {version}")
        self.destroy()
