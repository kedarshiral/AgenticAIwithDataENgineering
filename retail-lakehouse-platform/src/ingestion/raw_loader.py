from pathlib import Path
import pandas as pd
from datetime import datetime


class RawLoader:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.landing_dir = (
            self.project_root
            / "data"
            / "L0_landing"
        )

        self.l0_dir = (
            self.project_root
            / "data"
            / "L0"
        )

    def run(self):

        batch_id = (
            datetime.now()
            .strftime(
                "%Y%m%d%H%M%S"
            )
        )

        for table_dir in self.landing_dir.iterdir():

            if not table_dir.is_dir():
                continue

            table_name = (
                table_dir.name
            )

            latest_file = list(
                table_dir.glob(
                    "*.parquet"
                )
            )[0]

            df = pd.read_parquet(
                latest_file
            )

            df[
                "batch_id"
            ] = batch_id

            df[
                "ingestion_timestamp"
            ] = datetime.now()

            df[
                "source_system"
            ] = table_name

            output_dir = (
                self.l0_dir
                / table_name
            )

            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            df.to_parquet(
                output_dir,
                partition_cols=[
                    "batch_id"
                ],
                index=False
            )

            print(
                f"L0 Created: {table_name}"
            )