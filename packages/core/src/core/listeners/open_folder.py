from typing import Literal, Optional

from core.components import BaseListener, listen_to
from core.events import Signal
from core.state import state
from core.utils import open_folder


class OpenFolderListener(BaseListener):
    @listen_to(Signal.CMD_OPEN_FOLDER)
    def handle_open_folder(
        self,
        target: Literal["servers", "launcher"] = "launcher",
        path: Optional[str] = None,
    ):
        if path:
            open_folder(path)
            return
        if target == "servers":
            open_folder(state.instances_dir)
        else:
            open_folder(state.app_dir)
