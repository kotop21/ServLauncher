import logging
import threading
from typing import Dict, Optional

from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.utils import find_java


class JavaCheckListener(BaseListener):
    @listen_to(Signal.CMD_CHECK_JAVA)
    def handle_check_java(
        self, server_data: Dict, target_version: Optional[str] = None
    ):
        def task():
            exists, path = find_java()
            if exists:
                logging.info(f"[Core-listener] Java found at: {path}")
                bus.emit(Signal.EVENT_JAVA_FOUND, server_data=server_data)
            else:
                logging.warning("[Core-listener] Java not found on the system.")
                bus.emit(Signal.EVENT_JAVA_NOT_FOUND)

        threading.Thread(target=task, daemon=True).start()
