import json

from src.metadata.metadata_constants import (
    CATALOG_DIR
)


class DataDictionaryBuilder:

    def __init__(self):

        self.catalog_dir = CATALOG_DIR

    # =====================================================
    # Auto Description Generator
    # =====================================================

    def generate_description(
        self,
        column_name
    ):

        return (

            column_name

            .replace("_", " ")

            .title()

        )

    # =====================================================
    # Build Data Dictionary
    # =====================================================

    def build_dictionary(self):

        data_dictionary = {}

        for metadata_file in self.catalog_dir.glob("*.json"):

            with open(metadata_file) as file:

                metadata = json.load(file)

            table_name = metadata["table_name"]

            data_dictionary[table_name] = {

                "table_name": table_name,

                "business_domain":

                    metadata.get(
                        "business_domain"
                    ),

                "owner":

                    metadata.get(
                        "owner"
                    ),

                "layer":

                    metadata.get(
                        "layer"
                    ),

                "columns": []

            }

            for column in metadata["columns"]:

                data_dictionary[

                    table_name

                ][

                    "columns"

                ].append(

                    {

                        "column_name":

                            column["column_name"],

                        "datatype":

                            column["datatype"],

                        "nullable":

                            column["nullable"],

                        "description":

                            self.generate_description(

                                column["column_name"]

                            ),

                        "business_definition":

                            "",

                        "pii":

                            False

                    }

                )

        output_file = (

            self.catalog_dir

            / "data_dictionary.json"

        )

        with open(

            output_file,

            "w"

        ) as file:

            json.dump(

                data_dictionary,

                file,

                indent=4

            )

        print(

            "Data Dictionary Generated."

        )


if __name__ == "__main__":

    DataDictionaryBuilder().build_dictionary()