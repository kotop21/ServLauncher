from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state


class StopServerListener(BaseListener):
    @listen_to(Signal.CMD_STOP_SERVER)
    def handle_stop(self, server_id: int):
        process = state.get_process(server_id)
        if process and process.poll() is None:
            try:
                if process.stdin:
                    process.stdin.write("stop\n")
                    process.stdin.flush()
                    state.add_console_line(server_id, "> stop (sent by launcher)")
                    bus.emit(
                        Signal.SERVER_CONSOLE_OUTPUT,
                        server_id=server_id,
                        line="> stop (sent by launcher)",
                    )
            except Exception as e:
                print(
                    f"[Core-listener] Failed to send stop command to server {server_id}: {e}"
                )
                process.terminate()

    @listen_to(Signal.CMD_SHUTDOWN_ALL)
    def handle_shutdown_all(self):
        for server_id, process in list(state.active_processes.items()):
            if process.poll() is None:
                try:
                    if process.stdin:
                        process.stdin.write("stop\n")
                        process.stdin.flush()
                except:
                    process.terminate()

            try:
                process.wait(timeout=3)
            except:
                process.kill()

            state.remove_process(server_id)
            state.update_server_status(server_id, "Stopped")
        print("[Core-listener] All active servers have been shut down.")
