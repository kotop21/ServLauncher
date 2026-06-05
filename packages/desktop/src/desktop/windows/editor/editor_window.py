import re
from tkinter import messagebox

import customtkinter as ctk
from core.events import Signal, bus
from desktop.components import BaseWindow
from ttkbootstrap_icons_lucide import LucideIcon


class EditorWindow(BaseWindow):
    def __init__(self, master, path: str, content: str, server_id: int, **kwargs):
        self.path = path
        self.server_id = server_id
        self.initial_content = content

        filename = path.split("/")[-1] if "/" in path else path.split("\\")[-1]

        super().__init__(
            parent=master,
            title=f"Editor - {filename}",
            size=(700, 500),
            window_key=f"editor_{server_id}",
            resizable=(True, True),
            **kwargs,
        )

        self.minsize(400, 300)
        self.transient(master)

        self.top_bar = ctk.CTkFrame(self, height=40, fg_color="transparent")
        self.top_bar.pack(fill="x", padx=10, pady=(10, 5))

        self.lbl_path = ctk.CTkLabel(self.top_bar, text=filename, font=("", 14, "bold"))
        self.lbl_path.pack(side="left")

        self.icon_save = LucideIcon("save", size=16, color="#FFFFFF").image
        self.btn_save = ctk.CTkButton(
            self.top_bar,
            text="Save",
            image=self.icon_save,
            width=80,
            height=30,
            command=self.save_file,
        )
        self.btn_save.pack(side="right")

        self.bottom_bar = ctk.CTkFrame(self, height=25, fg_color="transparent")
        self.bottom_bar.pack(side="bottom", fill="x", padx=10, pady=(0, 5))

        self.btn_toggle_bool = ctk.CTkButton(
            self.bottom_bar,
            text="",
            width=60,
            height=20,
            font=("", 11),
            command=self.toggle_bool_value,
        )
        self.btn_toggle_bool.pack(side="left", padx=(0, 10))
        self.btn_toggle_bool.pack_forget()

        self.lbl_cursor = ctk.CTkLabel(
            self.bottom_bar, text="Ln 1, Col 1", font=("", 12), text_color="gray50"
        )
        self.lbl_cursor.pack(side="right")

        self.text_area = ctk.CTkTextbox(self, font=("Consolas", 13), wrap="none")
        self.text_area.pack(fill="both", expand=True, padx=10, pady=(0, 5))

        self.text_area._textbox.configure(undo=True, autoseparators=True, maxundo=-1)
        self.text_area.insert("1.0", content)

        self.setup_highlighting()
        self.highlight_syntax()
        self.update_cursor_info()

        self.text_area.bind("<KeyRelease>", self.on_key_release)
        self.text_area.bind("<ButtonRelease-1>", self.update_cursor_info)

        self.bind("<Control-s>", self._shortcut_save)
        self.bind("<Command-s>", self._shortcut_save)
        self.text_area.bind("<Control-z>", self._shortcut_undo)
        self.text_area.bind("<Command-z>", self._shortcut_undo)
        self.text_area.bind("<Control-y>", self._shortcut_redo)
        self.text_area.bind("<Command-Shift-z>", self._shortcut_redo)

        self._highlight_timer = None
        bus.subscribe(Signal.RESPONSE_FILE_SAVED, self.on_file_saved)

    def on_close(self):
        if self.text_area.get("1.0", "end-1c") != self.initial_content:
            if messagebox.askyesno(
                "Saving", "Do you want to save changes before exiting?"
            ):
                self.save_file()
                self.after(500, self.destroy)
            else:
                self.destroy()
        else:
            self.destroy()

    def setup_highlighting(self):
        self.text_area.tag_config("string", foreground="#A3BE8C")
        self.text_area.tag_config("key", foreground="#88C0D0")
        self.text_area.tag_config("number", foreground="#B48EAD")
        self.text_area.tag_config("boolean", foreground="#D08770")
        self.text_area.tag_config("comment", foreground="#4C566A")

    def highlight_syntax(self, _event=None):
        content = self.text_area.get("1.0", "end")
        for tag in ["string", "key", "number", "boolean", "comment"]:
            self.text_area.tag_remove(tag, "1.0", "end")
        patterns = {
            "comment": r"(#.*$|//.*$)",
            "string": r'(".*?"|\'.*?\')',
            "key": r"^\s*([a-zA-Z0-9_\-]+)\s*[:=]",
            "number": r"\b(\d+\.?\d*)\b",
            "boolean": r"\b(true|false|True|False)\b",
        }
        for tag, pattern in patterns.items():
            for match in re.finditer(pattern, content, re.MULTILINE):
                start_idx = f"1.0 + {match.start(1 if tag == 'key' else 0)}c"
                end_idx = f"1.0 + {match.end(1 if tag == 'key' else 0)}c"
                self.text_area.tag_add(tag, start_idx, end_idx)

    def update_cursor_info(self, _event=None):
        try:
            pos = self.text_area.index("insert")
            row, col = pos.split(".")
            self.lbl_cursor.configure(text=f"Ln {row}, Col {int(col) + 1}")
            self.check_for_bool(pos)
        except Exception:
            pass

    def check_for_bool(self, pos):
        word = self.text_area.get(f"{pos} wordstart", f"{pos} wordend").lower()
        if word in ["true", "false"]:
            self.btn_toggle_bool.configure(
                text=f"Switch to {'false' if word == 'true' else 'true'}"
            )
            self.btn_toggle_bool.pack(side="left", padx=(0, 10))
        else:
            self.btn_toggle_bool.pack_forget()

    def toggle_bool_value(self):
        pos = self.text_area.index("insert")
        word = self.text_area.get(f"{pos} wordstart", f"{pos} wordend")
        new_val = "false" if word.lower() == "true" else "true"
        if word[0].isupper():
            new_val = new_val.capitalize()
        self.text_area.delete(f"{pos} wordstart", f"{pos} wordend")
        self.text_area.insert(f"{pos} wordstart", new_val)
        self.highlight_syntax()
        self.update_cursor_info()

    def on_key_release(self, _event):
        self.update_cursor_info()
        if self._highlight_timer:
            self.after_cancel(self._highlight_timer)
        self._highlight_timer = self.after(300, self.highlight_syntax)

    def _shortcut_save(self, _event=None):
        self.save_file()
        return "break"

    def _shortcut_undo(self, _event=None):
        try:
            self.text_area._textbox.edit_undo()
            self.highlight_syntax()
            self.update_cursor_info()
        except Exception:
            pass
        return "break"

    def _shortcut_redo(self, _event=None):
        try:
            self.text_area._textbox.edit_redo()
            self.highlight_syntax()
            self.update_cursor_info()
        except Exception:
            pass
        return "break"

    def save_file(self):
        content = self.text_area.get("1.0", "end-1c")
        self.initial_content = content
        self.btn_save.configure(text="Saving...", state="disabled")
        bus.emit(
            Signal.CMD_SAVE_FILE,
            path=self.path,
            content=content,
            server_id=self.server_id,
        )

    def on_file_saved(self, path: str, server_id: int, success: bool):
        if server_id == self.server_id and path == self.path:
            self.btn_save.configure(
                text="Saved!" if success else "Error", state="normal"
            )
            self.after(2000, lambda: self.btn_save.configure(text="Save"))

    def destroy(self):
        try:
            bus.unsubscribe(Signal.RESPONSE_FILE_SAVED, self.on_file_saved)
        except Exception:
            pass
        super().destroy()
