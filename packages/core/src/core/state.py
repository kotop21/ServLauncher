import os
import tkinter.messagebox as messagebox
from collections import deque
from typing import Dict, List, Optional

from core.instance_storage import InstanceStorage


class CoreState(InstanceStorage):
    def __init__(self):
        super().__init__()
        self.filename = "instance.json"
        self.active_processes = {}
        self.console_buffers = {}
        self.servers: Dict[int, Dict] = self._load_data()

    def _load_data(self) -> Dict[int, Dict]:
        raw_data = self.load_json(self.filename, default={})
        parsed_data = {}
        for k, v in raw_data.items():
            server_id = int(k)
            v["status"] = "Stopped"
            v["process_key"] = None
            if "path" not in v:
                v["path"] = ""
            if "java_args" not in v:
                v["java_args"] = "-Xmx4G -Xms1G"
            parsed_data[server_id] = v
        return parsed_data

    def _sync_port(self, server_data: dict):
        prop_path = os.path.join(server_data["path"], "server.properties")
        if os.path.exists(prop_path):
            try:
                mtime = os.path.getmtime(prop_path)
                last_mtime = server_data.get("_last_prop_mtime", 0)

                if mtime <= last_mtime:
                    return

                with open(prop_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("server-port="):
                            port_str = line.split("=", 1)[1]
                            if port_str.isdigit():
                                port = int(port_str)
                                if server_data.get("port") != port:
                                    server_data["port"] = port
                                    print(
                                        f"[Core] Port synced to {port} for server {server_data['id']}"
                                    )
                                    self.save()
                                server_data["_last_prop_mtime"] = mtime
                                break
            except Exception as e:
                print(f"[Core] Failed to sync port for server {server_data['id']}: {e}")

    def save(self):
        data_to_save = {}
        for k, v in self.servers.items():
            save_copy = v.copy()
            save_copy.pop("status", None)
            save_copy.pop("process_key", None)
            save_copy.pop("is_imported", None)
            save_copy.pop("_last_prop_mtime", None)
            data_to_save[k] = save_copy
        self.save_json(self.filename, data_to_save)

    def get_all(self) -> List[Dict]:
        return list(self.servers.values())

    def get_server(self, server_id: int) -> Optional[Dict]:
        server = self.servers.get(server_id)
        if server:
            self._sync_port(server)
        return server

    def add_server(self, server_data: Dict) -> int:
        if server_data.get("path"):
            for existing in self.servers.values():
                if existing.get("path") == server_data["path"]:
                    messagebox.showerror(
                        "Error", "This server folder is already added to the launcher!"
                    )
                    return -1

        new_id = max(self.servers.keys(), default=0) + 1
        server_data["id"] = new_id
        server_data["status"] = "Stopped"
        server_data["process_key"] = None

        if not server_data.get("path"):
            server_data["path"] = self.create_instance_folder(
                new_id, server_data["name"]
            )

        if "java_args" not in server_data:
            server_data["java_args"] = "-Xmx4G -Xms1G"

        self.servers[new_id] = server_data
        self.save()
        return new_id

    def remove_server(self, server_id: int):
        if server_id in self.servers:
            self.remove_process(server_id)
            del self.servers[server_id]
            if server_id in self.console_buffers:
                del self.console_buffers[server_id]
            self.save()

    def update_server_status(self, server_id: int, new_status: str):
        if server_id in self.servers:
            self.servers[server_id]["status"] = new_status

    def update_server_java_args(self, server_id: int, java_args: str):
        if server_id in self.servers:
            self.servers[server_id]["java_args"] = java_args
            self.save()

    def delete_server(self, server_id: int):
        if server_id in self.servers:
            self.remove_process(server_id)
            path = self.servers[server_id].get("path")
            if path and str(path).startswith(str(self.instances_dir)):
                self.delete_instance_folder(path)
            del self.servers[server_id]
            if server_id in self.console_buffers:
                del self.console_buffers[server_id]
            self.save()

    def set_process(self, server_id: int, process):
        self.active_processes[server_id] = process
        self.console_buffers[server_id] = deque(maxlen=500)

    def get_process(self, server_id: int):
        return self.active_processes.get(server_id)

    def remove_process(self, server_id: int):
        if server_id in self.active_processes:
            del self.active_processes[server_id]

    def add_console_line(self, server_id: int, line: str):
        if server_id not in self.console_buffers:
            self.console_buffers[server_id] = deque(maxlen=500)
        self.console_buffers[server_id].append(line)

    def get_console_history(self, server_id: int) -> List[str]:
        if server_id in self.console_buffers:
            return list(self.console_buffers[server_id])
        return []


state = CoreState()
