import threading
from pathlib import Path
from core.events import bus, Signal
from core.components import BaseListener, listen_to
from core.state import state
from core.utils import run_jar


class StartServerListener(BaseListener):
    @listen_to(Signal.CMD_START_SERVER)
    def handle_start(self, server_id: int):
        server = state.get_server(server_id)
        if not server or server["status"] == "Running":
            return

        existing_process = state.get_process(server_id)
        if existing_process and existing_process.poll() is None:
            print(
                f"[Core-listener] Server {server_id} is already running in background!"
            )
            return

        server_dir = Path(server["path"])
        jar_path = server_dir / "server.jar"

        if not jar_path.exists():
            possible_jars = list(server_dir.glob("*.jar"))
            if not possible_jars:
                print(
                    f"[Core-listener] Error: No .jar files found for server {server_id} in {server_dir}"
                )
                return

            core_name = server.get("core", "").lower()
            matched_jar = None
            for j in possible_jars:
                name = j.name.lower()
                if core_name in name or "server" in name:
                    matched_jar = j
                    break

            jar_path = matched_jar if matched_jar else possible_jars[0]

        try:
            for lock_file in server_dir.rglob("session.lock"):
                if lock_file.exists():
                    try:
                        lock_file.unlink()
                    except OSError:
                        pass
        except Exception as e:
            print(f"[Core-listener] Error cleaning lock files: {e}")

        process = run_jar(str(jar_path), server.get("java_args", ""), str(server_dir))
        state.set_process(server_id, process)

        state.update_server_status(server_id, "Running")

        try:
            bus.emit(
                Signal.SERVER_STATUS_CHANGED, server_id=server_id, new_status="Running"
            )
        except RuntimeError:
            pass

        threading.Thread(
            target=self._monitor_output, args=(server_id, process), daemon=True
        ).start()

    def _monitor_output(self, server_id: int, process):
        for line in iter(process.stdout.readline, ""):
            clean_line = line.strip()
            if clean_line:
                state.add_console_line(server_id, clean_line)
                try:
                    bus.emit(
                        Signal.SERVER_CONSOLE_OUTPUT,
                        server_id=server_id,
                        line=clean_line,
                    )
                except RuntimeError:
                    pass

        process.wait()
        state.remove_process(server_id)
        state.update_server_status(server_id, "Stopped")

        try:
            bus.emit(
                Signal.SERVER_STATUS_CHANGED, server_id=server_id, new_status="Stopped"
            )
        except RuntimeError:
            pass
