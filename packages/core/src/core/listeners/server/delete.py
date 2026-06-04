from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.state import state


class DeleteServerListener(BaseListener):
    @listen_to(Signal.CMD_DELETE_SERVER)
    def handle_delete(self, server_id: int):
        print(f"[Core-listener] Deleting a server {server_id}...")

        state.delete_server(server_id)

        bus.emit(Signal.SERVER_DELETED, server_id=server_id)
