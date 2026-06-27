class MetadataValidator:

    def __init__(self):
        pass

    # ======================================================
    # Validate Metadata
    # ======================================================

    def validate(
        self,
        metadata
    ):

        errors = []

        # ---------------------------------------------

        if not metadata.get(
            "table_name"
        ):

            errors.append(
                "Missing table_name"
            )

        # ---------------------------------------------

        if metadata.get(
            "row_count",
            -1
        ) < 0:

            errors.append(
                "Invalid row count"
            )

        # ---------------------------------------------

        if metadata.get(
            "column_count",
            0
        ) == 0:

            errors.append(
                "No columns found"
            )

        # ---------------------------------------------

        if not metadata.get(
            "owner"
        ):

            errors.append(
                "Owner missing"
            )

        # ---------------------------------------------

        if not metadata.get(
            "business_domain"
        ):

            errors.append(
                "Business domain missing"
            )

        # ---------------------------------------------

        if metadata.get(
            "schema_version",
            0
        ) <= 0:

            errors.append(
                "Invalid schema version"
            )

        # ---------------------------------------------

        columns = metadata.get(
            "columns",
            []
        )

        names = [

            c["column_name"]

            for c in columns

        ]

        if len(names) != len(set(names)):

            errors.append(
                "Duplicate column names"
            )

        # ---------------------------------------------

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }