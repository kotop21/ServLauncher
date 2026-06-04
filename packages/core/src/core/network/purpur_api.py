import re

from .base_api import BaseAPI


class PurpurAPI(BaseAPI):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.purpurmc.org/v2"

    def _parse_version(self, v: str) -> tuple:
        main_part = v.split("-")[0]
        nums = [int(x) for x in re.findall(r"\d+", main_part)]

        while len(nums) < 4:
            nums.append(0)

        weight = 3
        suffix_num = 0

        if "-" in v:
            suffix = v.split("-", 1)[1].lower()
            if "rc" in suffix:
                weight = 2
            elif "pre" in suffix:
                weight = 1
            else:
                weight = 0

            s_nums = re.findall(r"\d+", suffix)
            if s_nums:
                suffix_num = int(s_nums[0])

        return (nums[0], nums[1], nums[2], nums[3], weight, suffix_num)

    def get_versions(self, project: str) -> list:
        url = f"{self.base_url}/{project}"
        data = self.fetch_json(url)
        versions = data.get("versions", [])
        return sorted(versions, key=self._parse_version, reverse=True)

    def get_builds(self, project: str, version: str) -> list:
        url = f"{self.base_url}/{project}/{version}"
        data = self.fetch_json(url)
        builds = data.get("builds", {}).get("all", [])

        def parse_build(b):
            try:
                return int(b)
            except ValueError:
                n = re.findall(r"\d+", str(b))
                return int(n[0]) if n else 0

        return sorted([str(b) for b in builds], key=parse_build, reverse=True)

    def get_download_url(self, project: str, version: str, build: str) -> str:
        build_id = build.split(" ")[0]
        return f"{self.base_url}/{project}/{version}/{build_id}/download"
