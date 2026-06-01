import os
import sys
import subprocess
from pathlib import Path


def open_folder(path: str | Path):
    path_str = str(path)
    if sys.platform == "win32":
        os.startfile(path_str)
        print("[Core-util] Open win32 folder")
    elif sys.platform == "darwin":
        subprocess.run(["open", path_str])
        print("[Core-util] Open darwin folder")
    else:
        subprocess.run(["xdg-open", path_str])
        print("[Core-util] Open xdg folder")
