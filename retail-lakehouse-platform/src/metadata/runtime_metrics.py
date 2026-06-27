import pandas as pd
from datetime import datetime

from src.metadata.metadata_constants import (
    RUNTIME_METRICS_FILE
)


class RuntimeMetrics:

    def __init__(self):

        self.metrics_file = RUNTIME_METRICS_FILE

        self.columns = [

            "batch_id",

            "table_name",

            "layer",

            "row_count",

            "column_count",

            "file_size_mb",

            "execution_time_seconds",

            "status",

            "refresh_time"

        ]

        self._initialize()

    # ==========================================================
    # Create runtime_metrics.csv
    # ==========================================================

    def _initialize(self):

        if self.metrics_file.exists():

            return

        df = pd.DataFrame(
            columns=self.columns
        )

        df.to_csv(
            self.metrics_file,
            index=False
        )

    # ==========================================================
    # Append Runtime Metrics
    # ==========================================================

    def log(
        self,
        metadata: dict,
        execution_time: float,
        status: str = "SUCCESS"
    ):

        df = pd.read_csv(
            self.metrics_file
        )

        new_row = {

            "batch_id":

                metadata["batch_id"],

            "table_name":

                metadata["table_name"],

            "layer":

                metadata["layer"],

            "row_count":

                metadata["row_count"],

            "column_count":

                metadata["column_count"],

            "file_size_mb":

                metadata["file_size_mb"],

            "execution_time_seconds":

                round(execution_time,2),

            "status":

                status,

            "refresh_time":

                datetime.utcnow().isoformat()

        }

        df.loc[len(df)] = new_row

        df.to_csv(

            self.metrics_file,

            index=False

        )

    # ==========================================================
    # Read Runtime Metrics
    # ==========================================================

    def load(self):

        return pd.read_csv(
            self.metrics_file
        )

    # ==========================================================
    # Latest Batch
    # ==========================================================

    def latest_batch(self):

        df = self.load()

        if df.empty:

            return None

        return df.iloc[-1].to_dict()

    # ==========================================================
    # Metrics By Table
    # ==========================================================

    def get_table_metrics(
        self,
        table_name
    ):

        df = self.load()

        return df[
            df.table_name == table_name
        ]