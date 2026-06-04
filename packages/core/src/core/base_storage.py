import json
import os
import platform
from pathlib import Path


class BaseStorage:
    def __init__(self, app_name: str = "ServLauncher"):
        self.app_dir = self._get_app_dir(app_name)
        self.app_dir.mkdir(parents=True, exist_ok=True)

    def _get_app_dir(self, app_name: str) -> Path:
        system = platform.system()
        if system == "Windows":
            base = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
        elif system == "Darwin":
            base = os.path.expanduser("~/Library/Application Support")
        else:
            base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))

        return Path(base) / app_name

    def get_path(self, filename: str) -> Path:
        return self.app_dir / filename

    def save_json(self, filename: str, data: dict):
        path = self.get_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_json(self, filename: str, default=None) -> dict:
        path = self.get_path(filename)
        if not path.exists():
            return default if default is not None else {}

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
