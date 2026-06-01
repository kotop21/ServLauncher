import subprocess
import shlex


def run_jar(jar_path: str, java_args: str, cwd: str) -> subprocess.Popen:
    args = ["java"] + shlex.split(java_args) + ["-jar", jar_path, "--nogui"]
    process = subprocess.Popen(
        args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    print(f"[Core-util] Run jar {jar_path} {java_args}")
    return process
