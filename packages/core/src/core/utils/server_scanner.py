import json
import re
import zipfile
from pathlib import Path


class ServerScanner:
    @staticmethod
    def scan(path: str) -> dict:
        p = Path(path)
        data = {
            "name": p.name,
            "core": "Unknown",
            "version": "Unknown",
            "build": "latest",
            "port": 25565,
            "path": str(p),
        }

        if not p.exists() or not p.is_dir():
            return data

        if (p / "purpur.yml").exists() or (p / "config" / "purpur.yml").exists():
            data["core"] = "Purpur"
        elif (
            (p / "paper.yml").exists()
            or (p / "config" / "paper-global.yml").exists()
            or (p / "paper-global.yml").exists()
        ):
            data["core"] = "Paper"
        elif (p / "spigot.yml").exists():
            data["core"] = "Spigot"
        elif (p / "bukkit.yml").exists():
            data["core"] = "Bukkit"

        props = p / "server.properties"
        if props.exists():
            try:
                with open(props, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.startswith("server-port="):
                            data["port"] = int(line.split("=")[1].strip())
                            break
            except Exception:
                pass

        server_jars = list(p.glob("*.jar"))
        for file in server_jars:
            name = file.name.lower()

            if (
                data["core"].lower() in name
                or "server" in name
                or len(server_jars) == 1
            ):
                try:
                    with zipfile.ZipFile(file, "r") as z:
                        if "version.json" in z.namelist():
                            with z.open("version.json") as vf:
                                v_data = json.load(vf)
                                if "id" in v_data:
                                    data["version"] = v_data["id"]
                                    break
                except Exception:
                    pass

                match = re.search(r"(\d+\.\d+(\.\d+)?)", name)
                if match:
                    data["version"] = match.group(1)
                    break

        return data
