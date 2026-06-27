from pathlib import Path
from datetime import datetime
import hashlib

import pandas as pd


class MetadataGenerator:

    def __init__(self):
        pass

    def generate(
        self,
        table_name: str,
        layer: str,
        file_path: str,
        batch_id: str,
        owner: str,
        business_domain: str,
        source_system: str,
        primary_key: str = None,
        foreign_keys: list = None
    ):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        # -----------------------------
        # Read Dataset
        # -----------------------------

        if file_path.suffix.lower() == ".csv":

            df = pd.read_csv(file_path)

        elif file_path.suffix.lower() == ".parquet":

            df = pd.read_parquet(file_path)

        elif file_path.suffix.lower() == ".json":

            df = pd.read_json(file_path)

        else:

            raise Exception(
                f"Unsupported file : {file_path}"
            )

        # -----------------------------
        # Column Metadata
        # -----------------------------

        columns = []

        schema_string = ""

        for column in df.columns:

            datatype = str(df[column].dtype)

            nullable = bool(df[column].isnull().any())

            unique = bool(df[column].is_unique)

            null_count = int(df[column].isnull().sum())

            column_metadata = {

                "column_name": column,

                "datatype": datatype,

                "nullable": nullable,

                "unique": unique,

                "null_count": null_count

            }

            columns.append(column_metadata)

            schema_string += f"{column}:{datatype};"

        # -----------------------------
        # Schema Hash
        # -----------------------------

        schema_hash = hashlib.md5(

            schema_string.encode()

        ).hexdigest()

        # -----------------------------
        # Dataset Metadata
        # -----------------------------

        metadata = {

            "table_name": table_name,

            "layer": layer,

            "batch_id": batch_id,

            "owner": owner,

            "business_domain": business_domain,

            "source_system": source_system,

            "primary_key": primary_key,

            "foreign_keys": foreign_keys or [],

            "row_count": int(len(df)),

            "column_count": int(len(df.columns)),

            "file_size_mb": round(
                file_path.stat().st_size / (1024 * 1024),
                2
            ),

            "schema_hash": schema_hash,

            "generated_at": datetime.utcnow().isoformat(),

            "columns": columns

        }

        return metadata