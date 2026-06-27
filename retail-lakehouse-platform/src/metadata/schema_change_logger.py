from datetime import datetime
import pandas as pd

from src.metadata.metadata_constants import (
    SCHEMA_CHANGE_LOG_FILE
)


class SchemaChangeLogger:

    def __init__(self):

        self.file = SCHEMA_CHANGE_LOG_FILE

        self.columns = [

            "timestamp",

            "table_name",

            "change_type",

            "column_name",

            "old_value",

            "new_value",

            "severity"

        ]

        self._initialize()

    # ======================================================
    # Create CSV
    # ======================================================

    def _initialize(self):

        if self.file.exists():

            return

        pd.DataFrame(
            columns=self.columns
        ).to_csv(
            self.file,
            index=False
        )

    # ======================================================
    # Severity Mapping
    # ======================================================

    def get_severity(
        self,
        change_type
    ):

        mapping = {

            "COLUMN_ADDED": "LOW",

            "COLUMN_REMOVED": "HIGH",

            "DATATYPE_CHANGED": "HIGH",

            "NULLABILITY_CHANGED": "MEDIUM",

            "PRIMARY_KEY_CHANGED": "CRITICAL",

            "FOREIGN_KEY_CHANGED": "CRITICAL"

        }

        return mapping.get(
            change_type,
            "LOW"
        )

    # ======================================================
    # Log Changes
    # ======================================================

    def log_changes(

        self,

        table_name,

        comparison_result

    ):

        if not comparison_result["changed"]:

            return

        df = pd.read_csv(
            self.file
        )

        for change in comparison_result["changes"]:

            row = {

                "timestamp":

                    datetime.utcnow().isoformat(),

                "table_name":

                    table_name,

                "change_type":

                    change["type"],

                "column_name":

                    change.get(
                        "column",
                        ""
                    ),

                "old_value":

                    change.get(
                        "old",
                        ""
                    ),

                "new_value":

                    change.get(
                        "new",
                        ""
                    ),

                "severity":

                    self.get_severity(
                        change["type"]
                    )

            }

            df.loc[len(df)] = row

        df.to_csv(
            self.file,
            index=False
        )