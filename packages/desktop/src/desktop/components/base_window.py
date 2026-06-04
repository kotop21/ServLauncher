import customtkinter as ctk


class BaseWindow(ctk.CTkToplevel):
    def __init__(
        self, parent, title="Launcher", size=(800, 600), saved_geometry=None, **kwargs
    ):
        root_master = parent.winfo_toplevel() if parent else None
        super().__init__(master=root_master, **kwargs)

        self.title(title)
        self.resizable(False, False)

        is_valid_geom = False
        if saved_geometry and isinstance(saved_geometry, str):
            try:
                w = int(saved_geometry.split("x")[0])
                h = int(saved_geometry.split("x")[1].split("+")[0].split("-")[0])
                if (
                    w >= 200
                    and h >= 200
                    and "+-" not in saved_geometry
                    and "-+" not in saved_geometry
                ):
                    is_valid_geom = True
            except Exception:
                pass

        if is_valid_geom:
            self.geometry(saved_geometry)
        else:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w // 2) - (size[0] // 2)
            y = (screen_h // 2) - (size[1] // 2)
            self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.focus()
