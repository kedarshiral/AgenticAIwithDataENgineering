from pathlib import Path
import json


class WatermarkManager:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.file_path = (
            self.project_root
            / "metadata"
            / "watermarks.json"
        )

    def load(self):

        if not self.file_path.exists():

            return {}

        with open(
            self.file_path,
            "r"
        ) as f:

            return json.load(f)

    def save(
        self,
        data
    ):

        with open(
            self.file_path,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )