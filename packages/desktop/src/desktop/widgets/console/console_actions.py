from typing import List

from core.events import Signal, bus


class ConsoleActions:
    def __init__(self, widget):
        self.widget = widget

    def start_server(self):
        bus.emit(Signal.CMD_START_SERVER, server_id=self.widget.server_data["id"])

    def stop_server(self):
        bus.emit(Signal.CMD_STOP_SERVER, server_id=self.widget.server_data["id"])

    def kill_server(self):
        bus.emit(Signal.CMD_KILL_SERVER, server_id=self.widget.server_data["id"])

    def send_command(self, event=None):
        if self.widget.server_data["status"] != "Running":
            return

        command = self.widget.entry_cmd.get().strip()
        if command:
            bus.emit(
                Signal.CMD_SEND_CONSOLE_COMMAND,
                server_id=self.widget.server_data["id"],
                command=command,
            )
            self.widget.entry_cmd.delete(0, "end")

    def on_console_output(self, server_id: int, line: str):
        if server_id == self.widget.server_data["id"]:
            self.widget.append_output(line)

    def on_history_received(self, server_id: int, history: List[str]):
        if server_id == self.widget.server_data["id"]:
            for line in history:
                self.widget.append_output(line)
