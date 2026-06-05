import logging
import traceback

import customtkinter as ctk


class BaseWindow(ctk.CTkToplevel):
    def __init__(
        self,
        parent,
        title="Launcher",
        size=(800, 600),
        resizable=(False, False),
        window_key=None,
        **kwargs,
    ):
        root_master = parent.winfo_toplevel() if parent else None
        super().__init__(master=root_master, **kwargs)

        self.withdraw()

        if root_master:
            self.transient(root_master)

        self.title(title)
        self.resizable(resizable[0], resizable[1])

        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = max(0, (screen_w // 2) - (size[0] // 2))
        y = max(0, (screen_h // 2) - (size[1] // 2))
        self.geometry(f"{size[0]}x{size[1]}+{int(x)}+{int(y)}")

        self.deiconify()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        logging.info(f"BaseWindow.on_close called for {self.__class__.__name__}")
        logging.debug(
            "BaseWindow.on_close stack:\n" + "".join(traceback.format_stack())
        )
        self.destroy()
