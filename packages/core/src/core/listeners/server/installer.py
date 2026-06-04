import threading
from pathlib import Path

from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.network.papermc_api import PaperMCAPI
from core.network.pufferfish_api import PufferfishAPI
from core.network.purpur_api import PurpurAPI
from core.state import state
from core.utils import accept_eula


class InstallerListener(BaseListener):
    def __init__(self):
        super().__init__()
        self.papermc = PaperMCAPI()
        self.purpur = PurpurAPI()
        self.pufferfish = PufferfishAPI()
        self._cancel_flags = {}

    def _get_api(self, core_name: str):
        c = core_name.lower()
        if c == "purpur":
            return self.purpur
        if c == "pufferfish":
            return self.pufferfish
        return self.papermc

    @listen_to(Signal.CMD_CANCEL_DOWNLOAD)
    def handle_cancel_download(self, server_id: int):
        self._cancel_flags[server_id] = True
        state.delete_server(server_id)
        bus.emit(Signal.CMD_REQUEST_ALL_SERVERS)

    @listen_to(Signal.CMD_FETCH_MC_VERSIONS)
    def handle_fetch_versions(self, core_name: str):
        def task():
            api = self._get_api(core_name)
            versions = api.get_versions(core_name.lower())
            bus.emit(
                Signal.RESPONSE_MC_VERSIONS, core_name=core_name, versions=versions
            )

        threading.Thread(target=task, daemon=True).start()

    @listen_to(Signal.CMD_FETCH_BUILD_VERSIONS)
    def handle_fetch_builds(self, core_name: str, mc_version: str):
        def task():
            api = self._get_api(core_name)
            builds = api.get_builds(core_name.lower(), mc_version)
            bus.emit(
                Signal.RESPONSE_BUILD_VERSIONS,
                core_name=core_name,
                mc_version=mc_version,
                builds=builds,
            )

        threading.Thread(target=task, daemon=True).start()

    @listen_to(Signal.CMD_ADD_SERVER)
    def handle_add_server(self, server_data: dict):
        new_id = state.add_server(server_data)

        if new_id == -1:
            return

        server = state.get_server(new_id)
        if not server:
            return

        bus.emit(Signal.SERVER_ADDED, server_data=server)

        bus.emit(
            Signal.EVENT_DOWNLOAD_STARTED,
            server_id=new_id,
            is_imported=server.get("is_imported", False),
            server_name=server["name"],
        )

        self._cancel_flags[new_id] = False

        if server.get("is_imported"):
            bus.emit(Signal.EVENT_DOWNLOAD_COMPLETE, server_id=new_id)
            return

        def task():
            api = self._get_api(server["core"])
            url = api.get_download_url(
                server["core"].lower(), server["version"], server["build"]
            )
            server_dir = server["path"]
            dest_path = str(Path(server_dir) / "server.jar")

            def progress(downloaded, total):
                if self._cancel_flags.get(new_id):
                    return
                bus.emit(
                    Signal.EVENT_DOWNLOAD_PROGRESS,
                    server_id=new_id,
                    downloaded=downloaded,
                    total=total,
                )

            success = api.download_file(url, dest_path, progress)

            if self._cancel_flags.get(new_id):
                if Path(dest_path).exists():
                    Path(dest_path).unlink()
                del self._cancel_flags[new_id]
                return

            if success:
                accept_eula(server_dir)
                bus.emit(Signal.EVENT_DOWNLOAD_COMPLETE, server_id=new_id)
            else:
                bus.emit(Signal.EVENT_DOWNLOAD_ERROR, server_id=new_id)

        threading.Thread(target=task, daemon=True).start()
