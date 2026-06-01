from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state


class ConsoleListener(BaseListener):
    @listen_to(Signal.CMD_SEND_CONSOLE_COMMAND)
    def handle_send_command(self, server_id: int, command: str):
        process = state.get_process(server_id)
        if process and process.stdin:
            try:
                process.stdin.write(command + "\n")
                process.stdin.flush()

                echo_line = f"> {command}"
                state.add_console_line(server_id, echo_line)
                bus.emit(
                    Signal.SERVER_CONSOLE_OUTPUT, server_id=server_id, line=echo_line
                )
            except Exception as e:
                print(
                    f"[Core-listener] Failed to send command to server {server_id}: {e}"
                )

    @listen_to(Signal.CMD_REQUEST_CONSOLE_HISTORY)
    def handle_request_history(self, server_id: int):
        history = state.get_console_history(server_id)
        bus.emit(Signal.RESPONSE_CONSOLE_HISTORY, server_id=server_id, history=history)
