from core.events import Signal, bus


class ServerSettingsActions:
    def __init__(self, window):
        self.window = window

    def save_args(self, event=None):
        current_args = self.window.entry_args.get("1.0", "end-1c").strip()
        if self.window.server_data.get("java_args") != current_args:
            self.window.server_data["java_args"] = current_args
            bus.emit(
                Signal.CMD_UPDATE_JAVA_ARGS,
                server_id=self.window.server_data["id"],
                java_args=current_args,
            )
        self.window.destroy()
        if event:
            return "break"
