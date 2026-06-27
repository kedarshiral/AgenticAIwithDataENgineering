from pathlib import Path
import pandas as pd
import yaml


class DQEngine:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.audit_dir = (
            self.project_root
            / "audit"
        )

        self.audit_dir.mkdir(
            exist_ok=True
        )

        with open(
            self.project_root
            / "configs"
            / "dq_rules.yaml",
            "r"
        ) as f:

            self.rules = yaml.safe_load(f)

        self.table_cache = {}

    # ==================================
    # LOAD TABLE
    # ==================================

    def load_table(
        self,
        table_name
    ):

        if table_name in self.table_cache:
            return self.table_cache[
                table_name
            ]

        data_dirs = [

            self.project_root
            / "data"
            / "source_local",

            self.project_root
            / "data"
            / "source_github"
        ]

        for directory in data_dirs:

            for file_path in directory.glob("*"):

                if file_path.stem != table_name:
                    continue

                if file_path.suffix == ".csv":

                    df = pd.read_csv(
                        file_path
                    )

                elif file_path.suffix == ".json":

                    df = pd.read_json(
                        file_path
                    )

                elif file_path.suffix == ".parquet":

                    df = pd.read_parquet(
                        file_path
                    )

                else:
                    continue

                self.table_cache[
                    table_name
                ] = df

                return df

        return None

    # ==================================
    # UNIQUE
    # ==================================

    def check_unique(
        self,
        df,
        column
    ):

        return (
            df[column]
            .duplicated()
            .sum()
        )

    # ==================================
    # NOT NULL
    # ==================================

    def check_not_null(
        self,
        df,
        column
    ):

        return (
            df[column]
            .isnull()
            .sum()
        )

    # ==================================
    # REGEX
    # ==================================

    def check_regex(
        self,
        df,
        column,
        pattern
    ):

        return (
            ~df[column]
            .astype(str)
            .str.match(pattern)
        ).sum()

    # ==================================
    # MIN VALUE
    # ==================================

    def check_min_value(
        self,
        df,
        column,
        min_value
    ):

        return (
            df[column]
            < min_value
        ).sum()

    # ==================================
    # FOREIGN KEY
    # ==================================

    def check_foreign_key(
        self,
        child_df,
        child_column,
        parent_df,
        parent_column
    ):

        return (
            ~child_df[
                child_column
            ].isin(
                parent_df[
                    parent_column
                ]
            )
        ).sum()

    # ==================================
    # RUN
    # ==================================

    def run(self):

        results = []

        tables = (
            self.rules[
                "tables"
            ]
        )

        for (
            table_name,
            columns
        ) in tables.items():

            df = self.load_table(
                table_name
            )

            if df is None:

                print(
                    f"{table_name} not found"
                )

                continue

            for (
                column_name,
                rules
            ) in columns.items():

                # -------------------
                # UNIQUE
                # -------------------

                if rules.get(
                    "unique"
                ):

                    failed = (
                        self.check_unique(
                            df,
                            column_name
                        )
                    )

                    results.append(
                        {
                            "table_name":
                            table_name,

                            "column_name":
                            column_name,

                            "rule_name":
                            "unique",

                            "status":
                            (
                                "PASS"
                                if failed == 0
                                else "FAIL"
                            ),

                            "failed_records":
                            failed
                        }
                    )

                # -------------------
                # NOT NULL
                # -------------------

                if rules.get(
                    "not_null"
                ):

                    failed = (
                        self.check_not_null(
                            df,
                            column_name
                        )
                    )

                    results.append(
                        {
                            "table_name":
                            table_name,

                            "column_name":
                            column_name,

                            "rule_name":
                            "not_null",

                            "status":
                            (
                                "PASS"
                                if failed == 0
                                else "FAIL"
                            ),

                            "failed_records":
                            failed
                        }
                    )

                # -------------------
                # REGEX
                # -------------------

                if (
                    "regex"
                    in rules
                ):

                    failed = (
                        self.check_regex(
                            df,
                            column_name,
                            rules[
                                "regex"
                            ]
                        )
                    )

                    results.append(
                        {
                            "table_name":
                            table_name,

                            "column_name":
                            column_name,

                            "rule_name":
                            "regex",

                            "status":
                            (
                                "PASS"
                                if failed == 0
                                else "FAIL"
                            ),

                            "failed_records":
                            failed
                        }
                    )

                # -------------------
                # MIN VALUE
                # -------------------

                if (
                    "min_value"
                    in rules
                ):

                    failed = (
                        self.check_min_value(
                            df,
                            column_name,
                            rules[
                                "min_value"
                            ]
                        )
                    )

                    results.append(
                        {
                            "table_name":
                            table_name,

                            "column_name":
                            column_name,

                            "rule_name":
                            "min_value",

                            "status":
                            (
                                "PASS"
                                if failed == 0
                                else "FAIL"
                            ),

                            "failed_records":
                            failed
                        }
                    )

                # -------------------
                # FOREIGN KEY
                # -------------------

                if (
                    "foreign_key"
                    in rules
                ):

                    parent_table = (
                        rules[
                            "foreign_key"
                        ][
                            "table"
                        ]
                    )

                    parent_column = (
                        rules[
                            "foreign_key"
                        ][
                            "column"
                        ]
                    )

                    parent_df = (
                        self.load_table(
                            parent_table
                        )
                    )

                    failed = (
                        self.check_foreign_key(
                            df,
                            column_name,
                            parent_df,
                            parent_column
                        )
                    )

                    results.append(
                        {
                            "table_name":
                            table_name,

                            "column_name":
                            column_name,

                            "rule_name":
                            "foreign_key",

                            "status":
                            (
                                "PASS"
                                if failed == 0
                                else "FAIL"
                            ),

                            "failed_records":
                            failed
                        }
                    )

        results_df = pd.DataFrame(
            results
        )

        results_df.to_csv(
            self.audit_dir
            / "dq_results.csv",
            index=False
        )

        print(
            "\nDQ Results Generated"
        )

        print(
            results_df
            .groupby(
                "status"
            )
            .size()
        )


if __name__ == "__main__":

    DQEngine().run()