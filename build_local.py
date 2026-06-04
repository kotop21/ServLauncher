import subprocess
import sys


def build():
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    subprocess.run(
        ["uv", "run", "python", ".github/scripts/freeze_versions.py"], check=True
    )

    cmd = [
        "uv",
        "run",
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name",
        "AstraLauncher",
        "--paths",
        "packages/core/src",
        "--paths",
        "packages/desktop/src",
        "--collect-all",
        "customtkinter",
        "--collect-all",
        "ttkbootstrap_icons",
        "--collect-all",
        "ttkbootstrap_icons_lucide",
        "packages/desktop/src/desktop/app.py",
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    build()
