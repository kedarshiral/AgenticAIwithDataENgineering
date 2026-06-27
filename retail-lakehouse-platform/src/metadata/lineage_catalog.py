import json
from pathlib import Path

import yaml

from src.metadata.metadata_constants import (
    LINEAGE_CATALOG_FILE
)


class LineageCatalogBuilder:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.lineage_yaml = (
            self.project_root
            / "configs"
            / "lineage.yaml"
        )

        self.output_file = (
            LINEAGE_CATALOG_FILE
        )

    # ==========================================================
    # Build Lineage Catalog
    # ==========================================================

    def build_catalog(self):

        with open(
            self.lineage_yaml,
            "r"
        ) as file:

            lineage = yaml.safe_load(file)

        lineage_catalog = {}

        for table_name, config in lineage.items():

            lineage_catalog[table_name] = {

                "table_name": table_name,

                "layer": config.get(
                    "layer",
                    None
                ),

                "domain": config.get(
                    "domain",
                    None
                ),

                "owner": config.get(
                    "owner",
                    "Retail Data Engineering"
                ),

                "upstream": config.get(
                    "upstream",
                    []
                ),

                "downstream": config.get(
                    "downstream",
                    []
                ),

                "transformation": config.get(
                    "transformation",
                    None
                )

            }

        with open(
            self.output_file,
            "w"
        ) as file:

            json.dump(

                lineage_catalog,

                file,

                indent=4

            )

        print(

            f"Lineage Catalog Generated : {self.output_file}"

        )


if __name__ == "__main__":

    LineageCatalogBuilder().build_catalog()