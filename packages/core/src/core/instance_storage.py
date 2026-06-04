import os
import shutil

from core.base_storage import BaseStorage


class InstanceStorage(BaseStorage):
    def __init__(self, app_name: str = "ServLauncher"):
        super().__init__(app_name)
        self.instances_dir = self.app_dir / "instances"
        self.instances_dir.mkdir(parents=True, exist_ok=True)

    def create_instance_folder(self, server_id: int, name: str) -> str:
        safe_name = "".join(
            c for c in name if c.isalnum() or c in (" ", "-", "_")
        ).strip()
        folder_name = f"{server_id}_{safe_name}"
        server_dir = self.instances_dir / folder_name
        server_dir.mkdir(parents=True, exist_ok=True)
        return str(server_dir)

    def delete_instance_folder(self, path: str):
        if path and os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)
