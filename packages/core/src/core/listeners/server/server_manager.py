from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.state import state


class ServerManagerListener(BaseListener):
    @listen_to(Signal.CMD_REMOVE_SERVER)
    def handle_remove_server(self, server_id: int):
        state.remove_server(server_id)
        bus.emit(Signal.CMD_REQUEST_ALL_SERVERS)

    @listen_to(Signal.CMD_DELETE_SERVER)
    def handle_delete_server(self, server_id: int):
        state.delete_server(server_id)
        bus.emit(Signal.CMD_REQUEST_ALL_SERVERS)
