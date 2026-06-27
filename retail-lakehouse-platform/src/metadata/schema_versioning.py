import json
from pathlib import Path
from datetime import datetime

from src.metadata.metadata_constants import (
    HISTORY_DIR,
    DEFAULT_SCHEMA_VERSION
)


class SchemaVersionManager:

    def __init__(self):

        self.history_dir = HISTORY_DIR

    # ==========================================================
    # Get Current Version
    # ==========================================================

    def get_current_version(
        self,
        metadata: dict
    ):

        return metadata.get(
            "schema_version",
            DEFAULT_SCHEMA_VERSION
        )

    # ==========================================================
    # Should Increase Version?
    # ==========================================================

    def should_increment(
        self,
        comparison_result: dict
    ):

        structural_changes = {

            "COLUMN_ADDED",

            "COLUMN_REMOVED",

            "DATATYPE_CHANGED",

            "NULLABILITY_CHANGED",

            "PRIMARY_KEY_CHANGED",

            "FOREIGN_KEY_CHANGED"

        }

        for change in comparison_result["changes"]:

            if change["type"] in structural_changes:

                return True

        return False

    # ==========================================================
    # Increment Version
    # ==========================================================

    def increment(
        self,
        metadata: dict
    ):

        metadata["schema_version"] = (

            metadata.get(
                "schema_version",
                DEFAULT_SCHEMA_VERSION
            )

            + 1

        )

        metadata["last_schema_change"] = (

            datetime.utcnow().isoformat()

        )

        return metadata

    # ==========================================================
    # Save History
    # ==========================================================

    def save_history(
        self,
        metadata: dict
    ):

        table_name = metadata["table_name"]

        version = metadata["schema_version"]

        output_dir = (

            self.history_dir /

            table_name

        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (

            output_dir /

            f"v{version}.json"

        )

        with open(
            output_file,
            "w"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )