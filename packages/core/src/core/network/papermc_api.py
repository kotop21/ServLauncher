import re

from .base_api import BaseAPI


class PaperMCAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.papermc.io/v2/projects"

    def _parse_version(self, v: str) -> tuple:
        nums = [int(x) for x in re.findall(r"\d+", v)]
        is_release = 1 if not re.search(r"[a-zA-Z]", v) else 0
        while len(nums) < 4:
            nums.append(0)
        return (nums[0], nums[1], nums[2], is_release, nums[3])

    def get_versions(self, project: str) -> list:
        url = f"{self.base_url}/{project}"
        data = self.fetch_json(url)
        versions = data.get("versions", [])
        return sorted(versions, key=self._parse_version, reverse=True)

    def get_builds(self, project: str, version: str) -> list:
        url = f"{self.base_url}/{project}/versions/{version}/builds"
        data = self.fetch_json(url)
        builds_data = data.get("builds", [])

        def parse_build(b):
            val = b.get("build", 0)
            try:
                return int(val)
            except ValueError:
                n = re.findall(r"\d+", str(val))
                return int(n[0]) if n else 0

        builds_data = sorted(builds_data, key=parse_build, reverse=True)

        result = []
        for b in builds_data:
            build_id = str(b.get("build"))
            result.append(build_id)
        return result

    def get_download_url(self, project: str, version: str, build: str) -> str:
        filename = f"{project}-{version}-{build}.jar"
        return f"{self.base_url}/{project}/versions/{version}/builds/{build}/downloads/{filename}"
