from core.components import BaseListener, listen_to
from core.events import Signal, bus
from core.utils.user_file_manager import UserFileManager


class UserFileManagerListener(BaseListener):
    @listen_to(Signal.CMD_READ_FILE)
    def handle_read(self, path: str, server_id: int):
        success, content = UserFileManager.read_file(path)
        bus.emit(
            Signal.RESPONSE_FILE_CONTENT,
            path=path,
            content=content,
            server_id=server_id,
            success=success,
        )

    @listen_to(Signal.CMD_SAVE_FILE)
    def handle_save(self, path: str, content: str, server_id: int):
        success = UserFileManager.save_file(path, content)
        bus.emit(
            Signal.RESPONSE_FILE_SAVED,
            path=path,
            server_id=server_id,
            success=success,
        )
