import tkinter.messagebox as messagebox

from core.events import Signal, bus

from desktop.windows import MainWindow


def main():
    app = MainWindow()

    def on_active_servers_status(has_active: bool):
        if not has_active:
            app.destroy()
            return

        if messagebox.askyesno(
            "Exit",
            "Are you sure you want to exit? All running servers will be stopped.",
        ):
            print("[Desktop] Initiating graceful shutdown for all servers...")
            bus.emit(Signal.CMD_SHUTDOWN_ALL)
            app.destroy()

    bus.subscribe(Signal.RESPONSE_ACTIVE_SERVERS_STATUS, on_active_servers_status)

    def on_closing():
        bus.emit(Signal.CMD_CHECK_ACTIVE_SERVERS)

    app.protocol("WM_DELETE_WINDOW", on_closing)

    print("[Desktop] Starting desktop launcher!")
    app.mainloop()

    bus.unsubscribe(Signal.RESPONSE_ACTIVE_SERVERS_STATUS, on_active_servers_status)


if __name__ == "__main__":
    main()
