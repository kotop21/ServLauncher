import os
import subprocess
import sys
from pathlib import Path


def open_folder(path: str | Path):
    path_str = str(path)
    if sys.platform == "win32":
        os.startfile(path_str)
        print(f"[Core-util] Open win32 folder: {path}")
    elif sys.platform == "darwin":
        subprocess.run(["open", path_str])
        print(f"[Core-util] Open darwin folder: {path}")
    else:
        subprocess.run(["xdg-open", path_str])
        print(f"[Core-util] Open xdg folder {path}")
