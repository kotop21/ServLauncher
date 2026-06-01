import sys
from pathlib import Path

__version__ = "dev-core"

if not getattr(sys, "frozen", False):
    import tomllib

    toml_path = Path(__file__).resolve().parents[3] / "pyproject.toml"

    if toml_path.exists():
        try:
            with open(toml_path, "rb") as f:
                __version__ = (
                    tomllib.load(f).get("project", {}).get("version", __version__)
                )
        except Exception:
            pass
