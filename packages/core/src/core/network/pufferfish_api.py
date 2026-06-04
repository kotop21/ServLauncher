import re

from .base_api import BaseAPI


class PufferfishAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.base_url = "https://ci.pufferfish.host"

    def _parse_version(self, v: str) -> tuple:
        nums = [int(x) for x in re.findall(r"\d+", v)]
        while len(nums) < 4:
            nums.append(0)
        return tuple(nums)

    def get_versions(self, project: str) -> list:
        url = f"{self.base_url}/api/json"
        data = self.fetch_json(url)
        jobs = data.get("jobs", [])
        versions = []
        for job in jobs:
            name = job.get("name", "")
            if name.startswith("Pufferfish-"):
                version = name.replace("Pufferfish-", "")
                if "1." in version:
                    versions.append(version)
        return sorted(versions, key=self._parse_version, reverse=True)

    def get_builds(self, project: str, version: str) -> list:
        url = f"{self.base_url}/job/Pufferfish-{version}/api/json"
        data = self.fetch_json(url)
        builds_data = data.get("builds", [])

        def parse_build(b):
            return int(b.get("number", 0))

        builds_data = sorted(builds_data, key=parse_build, reverse=True)
        return [str(b.get("number")) for b in builds_data if "number" in b]

    def get_download_url(self, project: str, version: str, build: str) -> str:
        url = f"{self.base_url}/job/Pufferfish-{version}/{build}/api/json"
        data = self.fetch_json(url)
        artifacts = data.get("artifacts", [])
        for a in artifacts:
            fileName = a.get("fileName", "")
            if fileName.endswith(".jar"):
                rel_path = a.get("relativePath", "")
                return f"{self.base_url}/job/Pufferfish-{version}/{build}/artifact/{rel_path}"
        return ""
