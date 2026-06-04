from typing import Dict

from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.state import state


class UIUpdaterListener(BaseListener):
    def _broadcast_server_list(self, **kwargs):
        data = state.get_all()
        bus.emit(Signal.RESPONSE_ALL_SERVERS, data=data)

    @listen_to(Signal.SERVER_ADDED)
    def on_added(self, server_data: Dict):
        self._broadcast_server_list()

    @listen_to(Signal.SERVER_DELETED)
    def on_deleted(self, server_id: int):
        self._broadcast_server_list()

    @listen_to(Signal.SERVER_STATUS_CHANGED)
    def on_status_changed(self, server_id: int, new_status: str):
        self._broadcast_server_list()
