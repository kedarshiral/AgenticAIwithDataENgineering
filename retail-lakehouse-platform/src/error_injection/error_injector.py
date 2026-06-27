import random
import numpy as np


class ErrorInjector:

    def inject_null_email(
        self,
        df,
        rate
    ):

        sample_size = int(
            len(df) * rate
        )

        indices = random.sample(
            list(df.index),
            sample_size
        )

        df.loc[
            indices,
            "email"
        ] = None

        return df

    def inject_duplicate_customer_id(
        self,
        df,
        rate
    ):

        sample_size = int(
            len(df) * rate
        )

        indices = random.sample(
            list(df.index),
            sample_size
        )

        duplicate_value = (
            df.iloc[0]
            ["customer_id"]
        )

        df.loc[
            indices,
            "customer_id"
        ] = duplicate_value

        return df

    def inject_invalid_fk(
        self,
        df,
        column,
        rate
    ):

        sample_size = int(
            len(df) * rate
        )

        indices = random.sample(
            list(df.index),
            sample_size
        )

        df.loc[
            indices,
            column
        ] = 999999999

        return df

    def inject_negative_price(
        self,
        df,
        rate
    ):

        sample_size = int(
            len(df) * rate
        )

        indices = random.sample(
            list(df.index),
            sample_size
        )

        df.loc[
            indices,
            "price"
        ] = (
            -1
            * np.abs(
                df.loc[
                    indices,
                    "price"
                ]
            )
        )

        return df