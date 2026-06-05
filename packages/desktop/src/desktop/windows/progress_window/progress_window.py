import customtkinter as ctk
from desktop.components import BaseWindow


class ProgressWindow(BaseWindow):
    def __init__(
        self, master, title="Progress", text="Please wait...", on_cancel=None, **kwargs
    ):
        super().__init__(
            parent=master,
            title=title,
            size=(450, 160),
            window_key=None,
            resizable=(False, False),
            **kwargs,
        )

        self.transient(master)
        self.grab_set()

        self.on_cancel_callback = on_cancel
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        self.lbl_text = ctk.CTkLabel(self, text=text, font=("", 14))
        self.lbl_text.pack(pady=(20, 10), padx=20, fill="x")

        self.progress_bar = ctk.CTkProgressBar(self, mode="determinate", height=10)
        self.progress_bar.pack(pady=(0, 15), padx=20, fill="x")
        self.progress_bar.set(0)

        self.btn_cancel = ctk.CTkButton(
            self,
            text="Cancel",
            command=self._on_cancel,
            fg_color="transparent",
            border_width=1,
            width=100,
        )
        self.btn_cancel.pack(pady=(0, 15))

    def update_progress(self, current, total, text=None):
        if total > 0:
            self.progress_bar.set(current / total)
        if text:
            self.lbl_text.configure(text=text)
        self.update_idletasks()

    def set_indeterminate(self):
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

    def _on_cancel(self):
        if self.on_cancel_callback:
            self.on_cancel_callback()
        self.close()

    def close(self):
        self.grab_release()
        try:
            self.destroy()
        except Exception:
            pass
