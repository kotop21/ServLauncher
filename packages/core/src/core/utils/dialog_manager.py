import os
import tkinter as tk
from tkinter import filedialog

from core.app_config import config


class DialogManager:
    @staticmethod
    def ask_directory(title: str = "Select Directory") -> str:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        initial_dir = config.get("last_opened_dir", "/")
        path = filedialog.askdirectory(title=title, initialdir=initial_dir)

        if path:
            config.set("last_opened_dir", path)

        root.destroy()
        return path

    @staticmethod
    def ask_file(title: str = "Select File", filetypes: list = None) -> str:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        if filetypes is None:
            filetypes = [("All files", "*.*")]

        initial_dir = config.get("last_opened_dir", "/")
        path = filedialog.askopenfilename(
            title=title, filetypes=filetypes, initialdir=initial_dir
        )

        if path:
            config.set("last_opened_dir", os.path.dirname(path))

        root.destroy()
        return path
