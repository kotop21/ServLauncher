from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.state import state


class GetServersListener(BaseListener):
    @listen_to(Signal.CMD_REQUEST_ALL_SERVERS)
    def handle_request_all(self):
        data = state.get_all()
        bus.emit(Signal.RESPONSE_ALL_SERVERS, data=data)

    @listen_to(Signal.CMD_REQUEST_SERVER)
    def handle_request_single(self, server_id: int):
        data = state.get_server(server_id)
        if data:
            bus.emit(Signal.RESPONSE_SERVER, data=data)

    @listen_to(Signal.CMD_CHECK_ACTIVE_SERVERS)
    def handle_check_active_servers(self):
        has_active = len(state.active_processes) > 0
        bus.emit(Signal.RESPONSE_ACTIVE_SERVERS_STATUS, has_active=has_active)
