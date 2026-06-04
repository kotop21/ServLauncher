import customtkinter as ctk
from core.version import __version__ as core_version

from desktop.version import __version__ as desktop_version
from desktop.widgets import InstanceSelectorWidget, MenuBar, StatusBar


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.minsize(350, 200)

        if "dev" in desktop_version or "dev" in core_version:
            self.title("AstraLauncher (develop)")
        else:
            self.title(f"Astra Launcher v{desktop_version} (Core v{core_version})")

        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

        self.menu_bar = MenuBar(self)
        self.menu_bar.pack(side="top", fill="x")

        self.instance_selector = InstanceSelectorWidget(
            self, status_bar=self.status_bar, fg_color="transparent"
        )
        self.instance_selector.pack(
            side="top", fill="both", expand=True, padx=10, pady=10
        )
