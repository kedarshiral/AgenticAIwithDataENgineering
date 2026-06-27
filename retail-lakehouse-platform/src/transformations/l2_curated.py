from pathlib import Path
import pandas as pd


class L2CuratedTransformer:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.l1_dir = (
            self.project_root
            / "data"
            / "L1"
        )

        self.l2_dir = (
            self.project_root
            / "data"
            / "L2"
        )

    def clean_dataframe(
        self,
        df
    ):

        df = (
            df.drop_duplicates(
                subset=[
                    "record_hash"
                ]
            )
        )

        return df

    def run(self):

        for table_dir in self.l1_dir.iterdir():

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

            df = pd.read_parquet(
                latest_batch
            )

            batch_id = (
                latest_batch.name
                .split("=")[1]
            )

            df["batch_id"] = batch_id

            df = (
                self.clean_dataframe(
                    df
                )
            )

            output_dir = (
                self.l2_dir
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
                f"L2 Created: {table_name}"
            )