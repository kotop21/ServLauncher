import tomllib
from pathlib import Path


def freeze_package_version(package_name):
    base_dir = Path(__file__).resolve().parents[2] / "packages" / package_name
    toml_path = base_dir / "pyproject.toml"
    version_file = base_dir / "src" / package_name / "version.py"

    with open(toml_path, "rb") as f:
        version = tomllib.load(f)["project"]["version"]

    frozen_code = f'import sys\n\n__version__ = "{version}"\n'
    version_file.write_text(frozen_code, encoding="utf-8")
    print(f"[*] {package_name} frozen to v{version}")


if __name__ == "__main__":
    freeze_package_version("core")
    freeze_package_version("desktop")
