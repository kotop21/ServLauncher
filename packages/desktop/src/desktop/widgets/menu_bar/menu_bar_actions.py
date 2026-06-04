from core.events import Signal, bus


class MenuBarActions:
    def __init__(self, widget):
        self.widget = widget

    def open_all_servers_folder(self):
        bus.emit(Signal.CMD_OPEN_FOLDER, target="servers")

    def open_launcher_folder(self):
        bus.emit(Signal.CMD_OPEN_FOLDER, target="launcher")

    def open_repository(self):
        print("[Desktop] Action: Open launcher repository")

    def support_developer(self):
        print("[Desktop] Action: Support the developer")

    def report_issue(self):
        print("[Desktop] Action: Report an issue / suggest a feature")
