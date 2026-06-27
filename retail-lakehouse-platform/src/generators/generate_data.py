from pathlib import Path
import yaml
import pandas as pd

from src.generators.customers import CustomerGenerator
from src.generators.products import ProductGenerator
from src.generators.marketing import MarketingGenerator
from src.generators.inventory import InventoryGenerator
from src.generators.orders import OrderGenerator
from src.generators.finance import FinanceGenerator
from src.audit.audit_logger import AuditLogger
from src.error_injection.error_injector import ErrorInjector
from src.ingestion.watermark_manager import WatermarkManager

class RetailDataGenerator:

    def __init__(self):

        self.project_root = (
            Path(__file__)
            .resolve()
            .parents[2]
        )

        self.audit_logger = (
                    AuditLogger()
                )
        self.error_injector = (
                    ErrorInjector()
                )

        with open(
            self.project_root
            / "configs"
            / "sources.yaml",
            "r"
        ) as f:

            self.sources_config = yaml.safe_load(f)

    # =====================================
    # SAVE DATASET
    # =====================================

    def save_dataset(
        self,
        table_name,
        df
    ):

        source_info = (
            self.sources_config
            ["sources"]
            [table_name]
        )

        storage_type = (
            source_info
            ["storage_type"]
        )

        file_format = (
            source_info
            ["format"]
        )

        if storage_type == "github":

            output_path = (
                self.project_root
                / "data"
                / "source_github"
            )

        elif storage_type == "local":

            output_path = (
                self.project_root
                / "data"
                / "source_local"
            )

        else:
            return

        output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            output_path
            /
            f"{table_name}.{file_format}"
        )

        if file_format == "csv":

            df.to_csv(
                file_path,
                index=False
            )

        elif file_format == "json":

            df.to_json(
                file_path,
                orient="records"
            )

        elif file_format == "parquet":

            df.to_parquet(
                file_path,
                index=False
            )

        print(
            f"✓ Saved {table_name}"
        )

        self.audit_logger.log(

                table_name=
                table_name,

                row_count=
                len(df),

                file_format=
                file_format,

                storage_type=
                storage_type,

                status=
                "SUCCESS"
            )

    # =====================================
    # PROCESS DOMAIN
    # =====================================

    def process_domain(
        self,
        datasets
    ):

        for (
            table_name,
            df
        ) in datasets.items():

            # ==================================
            # ERROR INJECTION (DISABLED)
            # ==================================

            # if table_name == "customers":
            
            #     df = (
            #         self.error_injector
            #         .inject_null_email(
            #             df,
            #             rate=0.01
            #         )
            #     )
            
            #     df = (
            #         self.error_injector
            #         .inject_duplicate_customer_id(
            #             df,
            #             rate=0.005
            #         )
            #     )

            # if table_name == "products":
            
            #     df = (
            #         self.error_injector
            #         .inject_negative_price(
            #             df,
            #             rate=0.005
            #         )
            #     )

            # if table_name == "orders":
            
            #     df = (
            #         self.error_injector
            #         .inject_invalid_fk(
            #             df,
            #             column="customer_id",
            #             rate=0.01
            #         )
            #     )

            self.save_dataset(
                table_name,
                df
            )

    # =====================================
    # GENERATE ALL
    # =====================================

    def generate_all(self):
        watermark_manager = (
            WatermarkManager()
        )

        watermarks = (
            watermark_manager.load()
        )
        print(watermarks)

        print("\nGenerating Customer Domain...")

        start_customer_id = (
            watermarks.get(
                "customers",
                0
            ) + 1
        )
        print("picked: ", start_customer_id)

        customer_generator = (
            CustomerGenerator(
                customer_count=50,
                start_customer_id=
                start_customer_id
            )
        )

        self.process_domain(
            customer_generator.generate()
        )

        watermarks[
            "customers"
        ] = (
            start_customer_id
            + 50
            - 1
        )

        # watermark_manager.save(
        #     watermarks
        # )
        # self.process_domain(
        #     CustomerGenerator().generate()
        # )

        print("\nGenerating Product Domain...")
        # self.process_domain(
        #     ProductGenerator().generate()
        # )
        # watermark_manager = (
        #     WatermarkManager()
        # )

        # watermarks = (
        #     watermark_manager.load()
        # )

        start_product_id = (
            watermarks.get(
                "products",
                0
            ) + 1
        )

        product_generator = (
            ProductGenerator(
                product_count=5,
                start_product_id=
                start_product_id
            )
        )

        self.process_domain(
            product_generator.generate()
        )

        watermarks[
            "products"
        ] = (
            start_product_id
            + 5
            - 1
        )

        # watermark_manager.save(
        #     watermarks
        # )

        print("\nGenerating Marketing Domain...")
        # self.process_domain(
        #     MarketingGenerator().generate()
        # )
        # watermark_manager = (
        #     WatermarkManager()
        # )

        # watermarks = (
        #     watermark_manager.load()
        # )

        start_campaign_id = (
            watermarks.get(
                "campaigns",
                0
            ) + 1
        )

        campaign_generator = (
            MarketingGenerator(

            customer_count=
            watermarks["customers"],

            campaign_count=2,

            start_campaign_id=
            start_campaign_id

        )
        )

        self.process_domain(
            campaign_generator.generate()
        )

        watermarks[
            "campaigns"
        ] = (
            start_campaign_id
            + 2
            - 1
        )

        # watermark_manager.save(
        #     watermarks
        # )

        # print("\nGenerating Inventory Domain...")
        # self.process_domain(
        #     InventoryGenerator().generate()
        # )

        # print("\nGenerating Sales Domain...")

        # sales_domain = (
        #     OrderGenerator().generate()
        # )

        # self.process_domain(
        #     sales_domain
        # )

        print("\nGenerating Sales Domain...")

        # watermarks = (
        #     watermark_manager.load()
        # )

        start_order_id = (
            watermarks.get(
                "orders",
                0
            ) + 1
        )

        start_order_item_id = (
            watermarks.get(
                "order_items",
                0
            ) + 1
        )

        sales_domain = (
            OrderGenerator(

            customer_count=
            watermarks["customers"],

            product_count=
            watermarks["products"],

            campaign_count=2,

            start_campaign_id=
            start_campaign_id,

            order_count=100,

            start_order_id=
            start_order_id,

            start_order_item_id=
            start_order_item_id

        ).generate()
        )

        self.process_domain(
            sales_domain
        )

        watermarks[
            "orders"
        ] = (
            start_order_id
            + 100
            - 1
        )

        watermarks[
            "order_items"
        ] = int(
            sales_domain[
                "order_items"
            ]["order_item_id"]
            .max()
        )

        # watermark_manager.save(
        #     watermarks
        # )

        print("\nGenerating Finance Domain...")

        finance_domain = (
            FinanceGenerator(
                sales_domain["orders"],
                sales_domain["returns"]
            ).generate()
        )

        self.process_domain(
            finance_domain
        )

        print(
            "\nAll datasets generated successfully."
        )

        watermark_manager.save(
            watermarks
        )

if __name__ == "__main__":

    RetailDataGenerator() \
        .generate_all()