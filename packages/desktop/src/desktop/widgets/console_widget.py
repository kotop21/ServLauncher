import customtkinter as ctk
from ttkbootstrap_icons_lucide import LucideIcon
from core.events import bus, Signal


class ConsoleWidget(ctk.CTkFrame):
    def __init__(self, master, server_data, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.server_data = server_data

        self.icon_play = LucideIcon("play", size=16, color="#FFFFFF").image
        self.icon_stop = LucideIcon("square", size=16, color="#FFFFFF").image
        self.icon_kill = LucideIcon("power", size=16, color="#FFFFFF").image

        self.console_text = ctk.CTkTextbox(
            self, wrap="word", font=("Consolas", 13), height=350
        )
        self.console_text.pack(fill="both", expand=True, pady=(0, 10))

        self.console_text.tag_config("info", foreground="#A9A9A9")
        self.console_text.tag_config("warn", foreground="#FFD700")
        self.console_text.tag_config("error", foreground="#FF4C4C")

        self.console_text.insert(
            "end",
            "[00:00:01] [Server thread/INFO]: Starting minecraft server version 1.20.4\n",
            "info",
        )
        self.console_text.insert(
            "end",
            "[00:00:02] [Server thread/WARN]: Ambiguity between arguments\n",
            "warn",
        )
        self.console_text.insert(
            "end",
            "[00:00:03] [Server thread/ERROR]: Failed to bind to port!\n",
            "error",
        )
        self.console_text.configure(state="disabled")

        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.pack(fill="x")

        self.entry_cmd = ctk.CTkEntry(
            self.control_frame, placeholder_text="Enter server command...", height=35
        )
        self.entry_cmd.pack(side="left", fill="x", expand=True, padx=(0, 10))

        status = self.server_data["status"]

        self.btn_start = ctk.CTkButton(
            self.control_frame,
            text="Start",
            image=self.icon_play,
            width=70,
            height=35,
            state="normal" if status != "Running" else "disabled",
            command=self._action_start,
        )
        self.btn_start.pack(side="left", padx=2)

        self.btn_stop = ctk.CTkButton(
            self.control_frame,
            text="Stop",
            image=self.icon_stop,
            width=70,
            height=35,
            state="normal" if status == "Running" else "disabled",
            command=self._action_stop,
        )
        self.btn_stop.pack(side="left", padx=2)

        self.btn_kill = ctk.CTkButton(
            self.control_frame,
            text="Kill",
            image=self.icon_kill,
            width=70,
            height=35,
            state="normal" if status == "Running" else "disabled",
        )
        self.btn_kill.pack(side="left", padx=2)

    def _action_start(self):
        print(f"[UI] Кнопка Start нажата для сервера: {self.server_data['name']}")
        bus.emit(
            Signal.TEST_SIGNAL, data=f"Команда запуска для {self.server_data['name']}"
        )

    def _action_stop(self):
        print(f"[UI] Кнопка Stop нажата для сервера: {self.server_data['name']}")
