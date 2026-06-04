import json
import ssl
import urllib.request

import certifi


class BaseAPI:
    def __init__(self):
        self.headers = {"User-Agent": "AstraLauncher/3.0"}
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

    def fetch_json(self, url: str) -> dict:
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(
                req, context=self.ssl_context, timeout=10
            ) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"[Core-Network] Request failed for {url}: {e}")
            return {}

    def download_file(self, url: str, dest_path: str, progress_callback=None) -> bool:
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(
                req, context=self.ssl_context, timeout=30
            ) as response:
                total_size = int(response.getheader("Content-Length", 0))
                with open(dest_path, "wb") as out_file:
                    downloaded = 0
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        out_file.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            return True
        except Exception as e:
            print(f"[Core-Network] Download failed for {url}: {e}")
            return False
