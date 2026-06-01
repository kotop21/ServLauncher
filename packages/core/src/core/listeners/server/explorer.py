import os
from pathlib import Path
from core.events import bus, Signal
from core.components import BaseListener, listen_to


class ExplorerListener(BaseListener):
    @listen_to(Signal.CMD_REQUEST_DIRECTORY)
    def handle_request_directory(self, path: str):
        self._load_and_emit(path)

    @listen_to(Signal.CMD_CHECK_DIRECTORY_UPDATE)
    def handle_check_update(self, path: str, last_mtime: float):
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return

            current_mtime = os.stat(path_obj).st_mtime
            if current_mtime != last_mtime:
                self._load_and_emit(path, current_mtime)
        except Exception:
            pass

    def _load_and_emit(self, path: str, current_mtime: float = None):
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return

            if current_mtime is None:
                current_mtime = os.stat(path_obj).st_mtime

            items = []
            folders = []
            files = []

            for entry in os.scandir(path_obj):
                if entry.name.startswith("."):
                    continue
                if entry.is_dir():
                    folders.append(entry.name)
                else:
                    files.append(entry.name)

            folders.sort(key=str.lower)
            files.sort(key=str.lower)

            for f in folders:
                items.append(
                    {"name": f + "/", "is_dir": True, "path": str(path_obj / f)}
                )
            for f in files:
                items.append({"name": f, "is_dir": False, "path": str(path_obj / f)})

            bus.emit(
                Signal.RESPONSE_DIRECTORY,
                path=str(path),
                items=items,
                mtime=current_mtime,
            )
        except Exception as e:
            print(f"[Core-listener] Error reading directory {path}: {e}")
