import re

import customtkinter as ctk
from core.events import Signal, bus
from ttkbootstrap_icons_lucide import LucideIcon

from .console_actions import ConsoleActions


class ConsoleWidget(ctk.CTkFrame):
    def __init__(self, master, server_data, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.server_data = server_data
        self.actions = ConsoleActions(self)

        self.icon_play = LucideIcon("play", size=16, color="#FFFFFF").image
        self.icon_stop = LucideIcon("square", size=16, color="#FFFFFF").image
        self.icon_kill = LucideIcon("power", size=16, color="#FFFFFF").image
        self.icon_clear = LucideIcon("trash-2", size=16, color="#FFFFFF").image

        bg_color = ctk.ThemeManager.theme["CTkTextbox"]["fg_color"]

        self.console_text = ctk.CTkTextbox(
            self, wrap="word", font=("Consolas", 13), height=350, fg_color=bg_color
        )
        self.console_text.pack(fill="both", expand=True, pady=(0, 10))

        self.console_text.tag_config("info", foreground="#A9A9A9")
        self.console_text.tag_config("warn", foreground="#FFD700")
        self.console_text.tag_config("error", foreground="#FF4C4C")
        self.console_text.tag_config("user", foreground="#00FF00")

        self.console_text.configure(state="disabled")

        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(fill="x")

        self.entry_cmd = ctk.CTkEntry(self.control_frame, height=35)
        self.entry_cmd.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_cmd.bind("<Return>", self.actions.send_command)

        self.btn_clear = ctk.CTkButton(
            self.control_frame,
            text="",
            image=self.icon_clear,
            width=35,
            height=35,
            command=self._clear_console,
        )
        self.btn_clear.pack(side="left", padx=(0, 10))

        self.btn_start = ctk.CTkButton(
            self.control_frame,
            text="Start",
            image=self.icon_play,
            width=70,
            height=35,
            command=self.actions.start_server,
        )
        self.btn_start.pack(side="left", padx=2)

        self.btn_stop = ctk.CTkButton(
            self.control_frame,
            text="Stop",
            image=self.icon_stop,
            width=70,
            height=35,
            command=self.actions.stop_server,
        )
        self.btn_stop.pack(side="left", padx=2)

        self.btn_kill = ctk.CTkButton(
            self.control_frame,
            text="Kill",
            image=self.icon_kill,
            width=70,
            height=35,
            command=self.actions.kill_server,
        )
        self.btn_kill.pack(side="left", padx=2)

        self._update_buttons(self.server_data["status"])

        bus.subscribe(Signal.SERVER_STATUS_CHANGED, self._on_status_changed)
        bus.subscribe(Signal.SERVER_CONSOLE_OUTPUT, self.actions.on_console_output)
        bus.subscribe(Signal.RESPONSE_CONSOLE_HISTORY, self.actions.on_history_received)

        bus.emit(Signal.CMD_REQUEST_CONSOLE_HISTORY, server_id=self.server_data["id"])

    def destroy(self):
        try:
            bus.unsubscribe(Signal.SERVER_STATUS_CHANGED, self._on_status_changed)
            bus.unsubscribe(
                Signal.SERVER_CONSOLE_OUTPUT, self.actions.on_console_output
            )
            bus.unsubscribe(
                Signal.RESPONSE_CONSOLE_HISTORY, self.actions.on_history_received
            )
        except Exception:
            pass
        super().destroy()

    def _clear_console(self):
        if not self.winfo_exists():
            return
        self.console_text.configure(state="normal")
        self.console_text.delete("1.0", "end")
        self.console_text.configure(state="disabled")

    def _update_buttons(self, status: str):
        if not self.winfo_exists():
            return
        is_running = status == "Running"
        self.btn_start.configure(state="disabled" if is_running else "normal")
        self.btn_stop.configure(state="normal" if is_running else "disabled")
        self.btn_kill.configure(state="normal" if is_running else "disabled")

        if is_running:
            self.entry_cmd.configure(
                state="normal", placeholder_text="Enter server command..."
            )
        else:
            self.entry_cmd.configure(
                state="disabled", placeholder_text="Server is offline..."
            )

    def _on_status_changed(self, server_id: int, new_status: str):
        if server_id == self.server_data["id"]:
            self.server_data["status"] = new_status
            self._update_buttons(new_status)

    def append_output(self, line: str):
        if not self.winfo_exists():
            return

        clean_line = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", line)

        self.console_text.configure(state="normal")

        is_at_bottom = self.console_text.yview()[1] >= 0.99

        tag = "info"
        lower_line = clean_line.lower()
        if "warn" in lower_line:
            tag = "warn"
        elif "error" in lower_line or "exception" in lower_line:
            tag = "error"
        elif clean_line.startswith(">"):
            tag = "user"

        self.console_text.insert("end", clean_line + "\n", tag)

        if is_at_bottom:
            self.console_text.see("end")

        self.console_text.configure(state="disabled")
