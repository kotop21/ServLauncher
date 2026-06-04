import re
import tkinter as tk
import tkinter.messagebox as messagebox
from typing import List

from core.events import Signal, bus


class AddServerActions:
    def __init__(self, view):
        self.view = view
        self.all_versions: List[str] = []
        self.all_builds: List[str] = []

        self._setup_bindings()
        self._subscribe()

        self.on_core_selected(self.view.option_core.get())

    def _setup_bindings(self):
        self.view.option_core.configure(command=self.on_core_selected)
        self.view.entry_search_version.bind("<KeyRelease>", self.on_search_version)
        self.view.entry_search_build.bind("<KeyRelease>", self.on_search_build)

        self.view.version_listbox.bind("<<ListboxSelect>>", self.on_version_selected)

        self.view.btn_cancel.configure(command=self.view.destroy)
        self.view.btn_confirm.configure(command=self.on_confirm)

    def _subscribe(self):
        bus.subscribe(Signal.RESPONSE_MC_VERSIONS, self.on_versions_received)
        bus.subscribe(Signal.RESPONSE_BUILD_VERSIONS, self.on_builds_received)
        bus.subscribe(Signal.RESPONSE_DIR_DIALOG, self.on_dir_selected)
        bus.subscribe(Signal.RESPONSE_SERVER_SCANNED, self.on_scanned)

    def on_destroy(self, event):
        if str(event.widget) == str(self.view):
            try:
                bus.unsubscribe(Signal.RESPONSE_MC_VERSIONS, self.on_versions_received)
                bus.unsubscribe(Signal.RESPONSE_BUILD_VERSIONS, self.on_builds_received)
                bus.unsubscribe(Signal.RESPONSE_DIR_DIALOG, self.on_dir_selected)
                bus.unsubscribe(Signal.RESPONSE_SERVER_SCANNED, self.on_scanned)
            except ValueError:
                pass

    def on_core_selected(self, core_name: str):
        self.view.version_listbox.delete(0, tk.END)
        self.view.build_listbox.delete(0, tk.END)
        self.all_versions = []
        self.all_builds = []

        self.view.entry_search_version.delete(0, "end")
        self.view.entry_search_build.delete(0, "end")

        if core_name == "Import Local":
            self.view.btn_confirm.configure(text="Select Folder")
            self.view.entry_search_version.configure(state="disabled")
            self.view.entry_search_build.configure(state="disabled")

            self.view.version_listbox.insert(tk.END, "N/A (Import)")
            self.view.build_listbox.insert(tk.END, "N/A (Import)")
            return

        self.view.btn_confirm.configure(text="Confirm")
        self.view.entry_search_version.configure(state="normal")
        self.view.entry_search_build.configure(state="normal")

        self.view.version_listbox.insert(tk.END, "Loading...")
        self.view.build_listbox.insert(tk.END, "Waiting...")

        bus.emit(Signal.CMD_FETCH_MC_VERSIONS, core_name=core_name)

    def on_versions_received(self, core_name: str, versions: List[str]):
        def task():
            if self.view.option_core.get() != core_name:
                return

            def parse_v(v):
                nums = [int(x) for x in re.findall(r"\d+", v)]
                is_release = 1 if not re.search(r"[a-zA-Z]", v) else 0
                while len(nums) < 4:
                    nums.append(0)
                return (nums[0], nums[1], nums[2], is_release, nums[3])

            self.all_versions = sorted(versions, key=parse_v, reverse=True)
            self.render_versions(self.all_versions)

        self.view.after(0, task)

    def render_versions(self, versions_to_show: List[str]):
        self.view.version_listbox.delete(0, tk.END)

        if not versions_to_show:
            self.view.version_listbox.insert(tk.END, "No versions found")
            return

        for v in versions_to_show:
            self.view.version_listbox.insert(tk.END, v)

        self.view.version_listbox.yview_moveto(0)
        self.view.version_listbox.selection_set(0)
        self.on_version_selected()

    def on_search_version(self, event=None):
        query = self.view.entry_search_version.get().strip().lower()
        if not query:
            self.render_versions(self.all_versions)
            return

        filtered = [v for v in self.all_versions if query in v.lower()]
        self.render_versions(filtered)

    def on_version_selected(self, event=None):
        selection = self.view.version_listbox.curselection()
        if not selection:
            return

        mc_version = self.view.version_listbox.get(selection[0])
        if mc_version in ["Loading...", "No versions found", "N/A (Import)"]:
            return

        self.view.build_listbox.delete(0, tk.END)
        self.view.entry_search_build.delete(0, "end")
        self.all_builds = []

        self.view.build_listbox.insert(tk.END, "Loading...")

        core_name = self.view.option_core.get()
        bus.emit(
            Signal.CMD_FETCH_BUILD_VERSIONS, core_name=core_name, mc_version=mc_version
        )

    def on_builds_received(self, core_name: str, mc_version: str, builds: List[str]):
        def task():
            selection = self.view.version_listbox.curselection()
            if not selection:
                return
            current_v = self.view.version_listbox.get(selection[0])

            if self.view.option_core.get() != core_name or current_v != mc_version:
                return

            self.all_builds = builds
            self.render_builds(builds)

        self.view.after(0, task)

    def render_builds(self, builds_to_show: List[str]):
        self.view.build_listbox.delete(0, tk.END)

        if not builds_to_show:
            self.view.build_listbox.insert(tk.END, "No builds found")
            return

        for b in builds_to_show:
            self.view.build_listbox.insert(tk.END, b)

        self.view.build_listbox.yview_moveto(0)
        self.view.build_listbox.selection_set(0)

    def on_search_build(self, event=None):
        query = self.view.entry_search_build.get().strip().lower()
        if not query:
            self.render_builds(self.all_builds)
            return

        filtered = [b for b in self.all_builds if query in b.lower()]
        self.render_builds(filtered)

    def on_confirm(self):
        name = self.view.entry_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Server Name is required!")
            return

        core = self.view.option_core.get()
        if core == "Import Local":
            bus.emit(Signal.CMD_OPEN_DIR_DIALOG, title="Select Server Folder")
            return

        v_sel = self.view.version_listbox.curselection()
        b_sel = self.view.build_listbox.curselection()

        if not v_sel or not b_sel:
            messagebox.showerror("Error", "Please select both Version and Build!")
            return

        version = self.view.version_listbox.get(v_sel[0])
        build = self.view.build_listbox.get(b_sel[0])

        if version in ["Loading...", "No versions found"] or build in [
            "Loading...",
            "Waiting...",
            "No builds found",
        ]:
            messagebox.showerror(
                "Error", "Please wait for valid versions/builds to load."
            )
            return

        agree = messagebox.askyesno(
            "Minecraft EULA",
            "By installing this server, you must agree to the Minecraft EULA.\n\n"
            "Read it here: https://aka.ms/MinecraftEULA\n\n"
            "Do you agree to the EULA?",
        )

        if not agree:
            return

        server_data = {
            "name": name,
            "core": core,
            "version": version,
            "build": build,
            "port": 25565,
            "path": "",
        }

        bus.emit(Signal.CMD_ADD_SERVER, server_data=server_data)
        self.view.destroy()

    def on_dir_selected(self, path: str):
        def task():
            if not path:
                return
            bus.emit(Signal.CMD_SCAN_SERVER_DIR, path=path)

        self.view.after(0, task)

    def on_scanned(self, server_data: dict):
        def task():
            if server_data["core"] == "Unknown" and server_data["version"] == "Unknown":
                messagebox.showerror(
                    "Invalid Directory",
                    "This directory does not appear to be a valid Minecraft server.\nCould not find server .jar or configuration files.",
                )
                return

            custom_name = self.view.entry_name.get().strip()
            if custom_name:
                server_data["name"] = custom_name

            server_data["is_imported"] = True

            bus.emit(Signal.CMD_ADD_SERVER, server_data=server_data)
            self.view.destroy()

        self.view.after(0, task)
