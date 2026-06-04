from core.components import BaseListener, listen_to
from core.events import Signal
from core.state import state


class UpdateArgsListener(BaseListener):
    @listen_to(Signal.CMD_UPDATE_JAVA_ARGS)
    def handle_update_args(self, server_id: int, java_args: str):
        state.update_server_java_args(server_id, java_args)
