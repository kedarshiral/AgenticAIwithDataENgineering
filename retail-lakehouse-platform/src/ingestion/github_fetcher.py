from pathlib import Path
import pandas as pd
import yaml


class GitHubFetcher:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        with open(
            self.project_root
            / "configs"
            / "sources.yaml",
            "r"
        ) as f:

            self.sources = yaml.safe_load(f)

    def fetch(
        self,
        table_name
    ):

        source_info = (
            self.sources["sources"]
            [table_name]
        )

        github_url = (
            source_info["url"]
        )

        file_format = (
            source_info["format"]
        )

        if file_format == "csv":

            return pd.read_csv(
                github_url
            )

        elif file_format == "json":

            return pd.read_json(
                github_url
            )

        elif file_format == "parquet":

            return pd.read_parquet(
                github_url
            )

        raise ValueError(
            f"Unsupported format: {file_format}"
        )