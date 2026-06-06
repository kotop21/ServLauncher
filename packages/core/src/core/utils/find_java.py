import os
import platform
import shutil
import subprocess
from typing import List, Optional, Tuple


def _get_java_version(java_path: str) -> Optional[str]:
    try:
        result = subprocess.run(
            [java_path, "-version"], capture_output=True, text=True, check=True
        )
        for line in result.stderr.splitlines():
            if "version" in line:
                parts = line.split('"')
                if len(parts) >= 3:
                    return parts[1]
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        pass
    return None


def _check_version_match(found_version: str, target_version: str) -> bool:
    if target_version == "8" and found_version.startswith("1.8."):
        return True
    if (
        found_version.startswith(f"{target_version}.")
        or found_version == target_version
    ):
        return True
    return False


def find_java(target_version: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    candidates: List[str] = []
    system = platform.system()
    exe_name = "java.exe" if system == "Windows" else "java"

    java_home = os.environ.get("JAVA_HOME")
    if java_home:
        candidates.append(os.path.join(java_home, "bin", exe_name))

    in_path = shutil.which("java")
    if in_path:
        candidates.append(in_path)

    if system == "Darwin":
        try:
            res = subprocess.run(
                ["/usr/libexec/java_home"], capture_output=True, text=True, check=True
            )
            candidates.append(os.path.join(res.stdout.strip(), "bin", "java"))
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        mac_jvm_dir = "/Library/Java/JavaVirtualMachines/"
        if os.path.exists(mac_jvm_dir):
            for jvm in os.listdir(mac_jvm_dir):
                candidates.append(
                    os.path.join(mac_jvm_dir, jvm, "Contents/Home/bin/java")
                )

    elif system == "Windows":
        base_paths = [
            os.environ.get("ProgramFiles", "C:\\Program Files"),
            os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
        ]
        for base in base_paths:
            java_base = os.path.join(base, "Java")
            if os.path.exists(java_base):
                for folder in os.listdir(java_base):
                    candidates.append(os.path.join(java_base, folder, "bin", exe_name))

            adoptium_base = os.path.join(base, "Eclipse Adoptium")
            if os.path.exists(adoptium_base):
                for folder in os.listdir(adoptium_base):
                    candidates.append(
                        os.path.join(adoptium_base, folder, "bin", exe_name)
                    )

    elif system == "Linux":
        jvm_base = "/usr/lib/jvm/"
        if os.path.exists(jvm_base):
            for folder in os.listdir(jvm_base):
                candidates.append(os.path.join(jvm_base, folder, "bin", exe_name))

    valid_candidates = []
    seen = set()

    for cand in candidates:
        if cand and os.path.isfile(cand) and os.access(cand, os.X_OK):
            real_path = os.path.realpath(cand)
            if real_path not in seen:
                seen.add(real_path)
                valid_candidates.append(real_path)

    for cand in valid_candidates:
        version = _get_java_version(cand)
        if version:
            if target_version is None:
                return True, cand

            if _check_version_match(version, target_version):
                return True, cand

    return False, None
