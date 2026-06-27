from pathlib import Path
import pandas as pd

from src.transformations.l1_raw import (
    L1RawTransformer
)


class L0ToL1Loader:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.l0_dir = (
            self.project_root
            / "data"
            / "L0"
        )

        self.l1_dir = (
            self.project_root
            / "data"
            / "L1"
        )

        self.transformer = (
            L1RawTransformer()
        )

    def load(self):

        for table_dir in self.l0_dir.iterdir():

            if not table_dir.is_dir():
                continue

            table_name = (
                table_dir.name
            )

            batch_dirs = sorted(
                table_dir.glob(
                    "batch_id=*"
                )
            )

            latest_batch = (
                batch_dirs[-1]
            )

            df = pd.read_parquet(
                latest_batch
            )

            batch_id = (
                latest_batch.name
                .split("=")[1]
            )

            df["batch_id"] = batch_id

            df = (
                self.transformer
                .transform(
                    df,
                    source_system=
                    table_name,

                    batch_id=
                    batch_id
                )
            )

            output_dir = (
                self.l1_dir
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
                f"L1 Created: {table_name}"
            )