from pathlib import Path
import pandas as pd
import yaml

from src.ingestion.github_fetcher import GitHubFetcher


class LandingLoader:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.github_fetcher = (
            GitHubFetcher()
        )

        with open(
            self.project_root
            / "configs"
            / "sources.yaml",
            "r"
        ) as f:

            self.sources = yaml.safe_load(f)

        self.landing_dir = (
            self.project_root
            / "data"
            / "L0_landing"
        )

    def load_local(
        self,
        table_name,
        source_info
    ):

        source_dir = (
            self.project_root
            / "data"
            / "source_local"
        )

        file_format = (
            source_info["format"]
        )

        file_path = (
            source_dir
            /
            f"{table_name}.{file_format}"
        )

        if file_format == "csv":
            return pd.read_csv(file_path)

        elif file_format == "json":
            return pd.read_json(file_path)

        elif file_format == "parquet":
            return pd.read_parquet(file_path)

    def run(self):

        for (
            table_name,
            source_info
        ) in self.sources[
            "sources"
        ].items():

            storage_type = (
                source_info[
                    "storage_type"
                ]
            )

            if storage_type == "github":

                df = (
                    self.github_fetcher
                    .fetch(table_name)
                )

            else:

                df = (
                    self.load_local(
                        table_name,
                        source_info
                    )
                )

            output_dir = (
                self.landing_dir
                / table_name
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            output_file = (
                output_dir
                /
                f"{table_name}.parquet"
            )

            df.to_parquet(
                output_file,
                index=False
            )

            print(
                f"Landed: {table_name}"
            )