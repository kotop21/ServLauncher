from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.state import state


class KillServerListener(BaseListener):
    @listen_to(Signal.CMD_KILL_SERVER)
    def handle_kill(self, server_id: int):
        process = state.get_process(server_id)
        if process:
            process.kill()
            state.remove_process(server_id)

        state.update_server_status(server_id, "Stopped")
        bus.emit(
            Signal.SERVER_STATUS_CHANGED, server_id=server_id, new_status="Stopped"
        )
