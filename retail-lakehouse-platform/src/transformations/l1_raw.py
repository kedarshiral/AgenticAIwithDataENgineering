from datetime import datetime
import hashlib
import re


class L1RawTransformer:

    def standardize_columns(
        self,
        df
    ):

        df.columns = [

            re.sub(
                r'[^a-zA-Z0-9]',
                '_',
                col
            )
            .lower()

            for col in df.columns
        ]

        return df

    def generate_record_hash(
        self,
        df
    ):

        return df.astype(
            str
        ).apply(

            lambda row:

            hashlib.md5(

                "|".join(
                    row.values
                ).encode()

            ).hexdigest(),

            axis=1
        )

    def transform(
        self,
        df,
        source_system,
        batch_id
    ):

        df = (
            self.standardize_columns(
                df
            )
        )

        df[
            "source_system"
        ] = source_system

        df[
            "load_timestamp"
        ] = datetime.now()

        df[
            "record_hash"
        ] = self.generate_record_hash(
            df
        )

        return df