from copy import deepcopy

from src.metadata.metadata_constants import (
    NO_CHANGE,
    COLUMN_ADDED,
    COLUMN_REMOVED,
    DATATYPE_CHANGED,
    NULLABILITY_CHANGED,
    PRIMARY_KEY_CHANGED,
    FOREIGN_KEY_CHANGED
)


class MetadataComparator:

    def __init__(self):
        pass

    # ==========================================================
    # Compare Metadata
    # ==========================================================

    def compare(
        self,
        old_metadata: dict,
        new_metadata: dict
    ):

        result = {

            "changed": False,

            "changes": []

        }

        # ------------------------------------------
        # First Time Load
        # ------------------------------------------

        if old_metadata is None:

            result["changed"] = True

            result["changes"].append({

                "type": "FIRST_LOAD",

                "message": "New metadata created"

            })

            return result

        # ------------------------------------------
        # Primary Key
        # ------------------------------------------

        if old_metadata["primary_key"] != new_metadata["primary_key"]:

            result["changed"] = True

            result["changes"].append({

                "type": PRIMARY_KEY_CHANGED,

                "old": old_metadata["primary_key"],

                "new": new_metadata["primary_key"]

            })

        # ------------------------------------------
        # Foreign Keys
        # ------------------------------------------

        if sorted(old_metadata["foreign_keys"]) != sorted(new_metadata["foreign_keys"]):

            result["changed"] = True

            result["changes"].append({

                "type": FOREIGN_KEY_CHANGED,

                "old": old_metadata["foreign_keys"],

                "new": new_metadata["foreign_keys"]

            })

        # ------------------------------------------
        # Columns
        # ------------------------------------------

        old_columns = {

            c["column_name"]: deepcopy(c)

            for c in old_metadata["columns"]

        }

        new_columns = {

            c["column_name"]: deepcopy(c)

            for c in new_metadata["columns"]

        }

        # ------------------------------------------
        # Added Columns
        # ------------------------------------------

        for column in new_columns:

            if column not in old_columns:

                result["changed"] = True

                result["changes"].append({

                    "type": COLUMN_ADDED,

                    "column": column

                })

        # ------------------------------------------
        # Removed Columns
        # ------------------------------------------

        for column in old_columns:

            if column not in new_columns:

                result["changed"] = True

                result["changes"].append({

                    "type": COLUMN_REMOVED,

                    "column": column

                })

        # ------------------------------------------
        # Existing Columns
        # ------------------------------------------

        common_columns = (

            set(old_columns.keys())

            &

            set(new_columns.keys())

        )

        for column in common_columns:

            # datatype

            if (

                old_columns[column]["datatype"]

                !=

                new_columns[column]["datatype"]

            ):

                result["changed"] = True

                result["changes"].append({

                    "type": DATATYPE_CHANGED,

                    "column": column,

                    "old": old_columns[column]["datatype"],

                    "new": new_columns[column]["datatype"]

                })

            # nullable

            if (

                old_columns[column]["nullable"]

                !=

                new_columns[column]["nullable"]

            ):

                result["changed"] = True

                result["changes"].append({

                    "type": NULLABILITY_CHANGED,

                    "column": column,

                    "old": old_columns[column]["nullable"],

                    "new": new_columns[column]["nullable"]

                })

        # ------------------------------------------
        # No Change
        # ------------------------------------------

        if not result["changed"]:

            result["changes"].append({

                "type": NO_CHANGE,

                "message": "Schema unchanged"

            })

        return result