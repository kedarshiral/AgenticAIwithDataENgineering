import json
from pathlib import Path

from src.metadata.metadata_constants import (
    CATALOG_DIR
)


class MetadataCatalog:

    def __init__(self):

        self.catalog_dir = CATALOG_DIR

    # =====================================================
    # Save Metadata
    # =====================================================

    def save(self, metadata: dict):

        table_name = metadata["table_name"]

        output_file = (
            self.catalog_dir /
            f"{table_name}.json"
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

    # =====================================================
    # Load Metadata
    # =====================================================

    def load(
        self,
        table_name: str
    ):

        file_path = (
            self.catalog_dir /
            f"{table_name}.json"
        )

        if not file_path.exists():

            return None

        with open(file_path) as file:

            return json.load(file)

    # =====================================================
    # Metadata Exists?
    # =====================================================

    def exists(
        self,
        table_name: str
    ):

        return (
            self.catalog_dir /
            f"{table_name}.json"
        ).exists()

    # =====================================================
    # Delete Metadata
    # =====================================================

    def delete(
        self,
        table_name: str
    ):

        file_path = (
            self.catalog_dir /
            f"{table_name}.json"
        )

        if file_path.exists():

            file_path.unlink()

    # =====================================================
    # List All Tables
    # =====================================================

    def list_tables(self):

        return sorted(

            [

                file.stem

                for file

                in self.catalog_dir.glob("*.json")

            ]

        )

    # =====================================================
    # Read Entire Catalog
    # =====================================================

    def load_catalog(self):

        catalog = {}

        for table in self.list_tables():

            catalog[table] = self.load(table)

        return catalog