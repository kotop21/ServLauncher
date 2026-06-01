from pathlib import Path


class UserFileManager:
    @staticmethod
    def read_file(path: str) -> tuple[bool, str]:
        try:
            p = Path(path)
            if p.exists() and p.is_file():
                with open(p, "r", encoding="utf-8") as f:
                    return True, f.read()
            return False, ""
        except Exception as e:
            print(f"[Core-util] File read error: {e}")
            return False, ""

    @staticmethod
    def save_file(path: str, content: str) -> bool:
        try:
            p = Path(path)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"[Core-util] File save error: {e}")
            return False
