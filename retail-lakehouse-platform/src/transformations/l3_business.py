from pathlib import Path
import pandas as pd


class L3BusinessTransformer:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.l2_dir = (
            self.project_root
            / "data"
            / "L2"
        )

        self.l3_dir = (
            self.project_root
            / "data"
            / "L3"
        )

    def read_latest_batch(
        self,
        table_name
    ):

        table_dir = (
            self.l2_dir
            / table_name
        )

        batch_dirs = sorted(
            table_dir.glob(
                "batch_id=*"
            )
        )

        latest_batch = (
            batch_dirs[-1]
        )

        # return pd.read_parquet(
        #     latest_batch
        # )
    
        df = pd.read_parquet(
            latest_batch
        )

        batch_id = (
            latest_batch.name
            .split("=")[1]
        )

        df["batch_id"] = batch_id

        return df

    # ==========================
    # DIM CUSTOMER
    # ==========================

    def build_dim_customer(self):

        customers = (
            self.read_latest_batch(
                "customers"
            )
        )

        customer_addresses = (
            self.read_latest_batch(
                "customer_addresses"
            )
        )

        dim_customer = (
            customers.merge(
                customer_addresses,
                on="customer_id",
                how="left"
            )
        )

        dim_customer["batch_id"] = (
            dim_customer["batch_id_x"]
        )

        dim_customer.drop(
            columns=[
                "batch_id_x",
                "batch_id_y"
            ],
            inplace=True
        )

        return dim_customer

    # ==========================
    # DIM PRODUCT
    # ==========================

    def build_dim_product(self):

        products = (
            self.read_latest_batch(
                "products"
            )
        )

        return products

    # ==========================
    # FACT ORDERS
    # ==========================

    def build_fact_orders(self):

        orders = (
            self.read_latest_batch(
                "orders"
            )
        )

        order_items = (
            self.read_latest_batch(
                "order_items"
            )
        )

        fact_orders = (
            orders.merge(
                order_items,
                on="order_id",
                how="left"
            )
        )

        fact_orders["batch_id"] = (
            fact_orders["batch_id_x"]
        )

        fact_orders.drop(
            columns=[
                "batch_id_x",
                "batch_id_y"
            ],
            inplace=True
        )

        return fact_orders

    # ==========================
    # FACT PAYMENTS
    # ==========================

    def build_fact_payments(self):

        return (
            self.read_latest_batch(
                "payments"
            )
        )

    # ==========================
    # FACT RETURNS
    # ==========================

    def build_fact_returns(self):

        return (
            self.read_latest_batch(
                "returns"
            )
        )

    # ==========================
    # SAVE
    # ==========================

    def save_dataset(
        self,
        dataset_name,
        df
    ):

        # batch_id = (
        #     df["batch_id"]
        #     .iloc[0]
        # )

        output_dir = (
            self.l3_dir
            / dataset_name
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )
        
        df.to_parquet(
            output_dir,
            partition_cols=[
                "batch_id"
            ],
            index=False
        )

        print(
            f"L3 Created: {dataset_name}"
        )

    # ==========================
    # RUN
    # ==========================

    def run(self):

        self.save_dataset(
            "dim_customer",
            self.build_dim_customer()
        )

        self.save_dataset(
            "dim_product",
            self.build_dim_product()
        )

        self.save_dataset(
            "fact_orders",
            self.build_fact_orders()
        )

        self.save_dataset(
            "fact_payments",
            self.build_fact_payments()
        )

        self.save_dataset(
            "fact_returns",
            self.build_fact_returns()
        )