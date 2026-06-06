import logging
import traceback
from enum import Enum, auto
from typing import Callable, Dict, List


class Signal(Enum):
    CMD_ADD_SERVER = auto()
    CMD_DELETE_SERVER = auto()
    CMD_START_SERVER = auto()
    CMD_STOP_SERVER = auto()
    CMD_KILL_SERVER = auto()
    CMD_REQUEST_ALL_SERVERS = auto()
    CMD_REQUEST_SERVER = auto()
    CMD_UPDATE_JAVA_ARGS = auto()
    CMD_OPEN_FOLDER = auto()
    CMD_SHUTDOWN_ALL = auto()
    CMD_FETCH_MC_VERSIONS = auto()
    CMD_FETCH_BUILD_VERSIONS = auto()
    CMD_SEND_CONSOLE_COMMAND = auto()
    CMD_REQUEST_CONSOLE_HISTORY = auto()
    CMD_REQUEST_DIRECTORY = auto()
    CMD_CHECK_DIRECTORY_UPDATE = auto()
    CMD_READ_FILE = auto()
    CMD_SAVE_FILE = auto()
    CMD_OPEN_DIR_DIALOG = auto()
    CMD_SCAN_SERVER_DIR = auto()
    CMD_REMOVE_SERVER = auto()
    CMD_CANCEL_DOWNLOAD = auto()
    CMD_CHECK_ACTIVE_SERVERS = auto()
    CMD_CHECK_JAVA = auto()

    EVENT_DOWNLOAD_PROGRESS = auto()
    EVENT_DOWNLOAD_COMPLETE = auto()
    EVENT_DOWNLOAD_ERROR = auto()
    EVENT_JAVA_FOUND = auto()
    EVENT_JAVA_NOT_FOUND = auto()

    SERVER_ADDED = auto()
    SERVER_DELETED = auto()
    SERVER_STATUS_CHANGED = auto()
    SERVER_CONSOLE_OUTPUT = auto()

    RESPONSE_ALL_SERVERS = auto()
    RESPONSE_SERVER = auto()
    RESPONSE_CONSOLE_HISTORY = auto()
    RESPONSE_BUILD_VERSIONS = auto()
    RESPONSE_MC_VERSIONS = auto()
    RESPONSE_DIRECTORY = auto()
    RESPONSE_FILE_CONTENT = auto()
    RESPONSE_FILE_SAVED = auto()
    RESPONSE_SERVER_SCANNED = auto()
    RESPONSE_DIR_DIALOG = auto()
    RESPONSE_ACTIVE_SERVERS_STATUS = auto()

    EVENT_DOWNLOAD_STARTED = auto()


class StrictEventBus:
    def __init__(self):
        self._listeners: Dict[Signal, List[Callable]] = {sig: [] for sig in Signal}

    def subscribe(self, signal: Signal, callback: Callable):
        if not callable(callback):
            raise TypeError("Callback must be a callable function/method.")
        self._listeners[signal].append(callback)

    def unsubscribe(self, signal: Signal, callback: Callable):
        if callback in self._listeners[signal]:
            self._listeners[signal].remove(callback)

    def emit(self, signal: Signal, **kwargs):
        if not self._listeners[signal]:
            logging.error(
                f"[EventBus] Security Error: Signal {signal.name} was sent, "
                "but no one subscribed to it!"
            )
            raise RuntimeError(
                f"[EventBus] Security Error: Signal {signal.name} was sent, "
                "but no one subscribed to it!"
            )

        for callback in self._listeners[signal]:
            try:
                callback(**kwargs)
            except Exception as e:
                print(f"[EventBus] Error in callback {callback}: {e}")
                traceback.print_exc()


bus = StrictEventBus()
