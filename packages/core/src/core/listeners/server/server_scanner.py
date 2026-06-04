from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.utils.server_scanner import ServerScanner


class ServerScannerListener(BaseListener):
    @listen_to(Signal.CMD_SCAN_SERVER_DIR)
    def handle_scan(self, path: str):
        server_data = ServerScanner.scan(path)
        bus.emit(Signal.RESPONSE_SERVER_SCANNED, server_data=server_data)
