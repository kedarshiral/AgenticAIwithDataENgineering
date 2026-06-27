from faker import Faker
import pandas as pd
import random
import numpy as np
from datetime import datetime

fake = Faker()


class ProductGenerator:

    def __init__(
        self,
        brand_count=50,
        category_count=20,
        supplier_count=100,
        product_count=50,
        start_product_id=1
    ):

        self.brand_count = brand_count
        self.category_count = category_count
        self.supplier_count = supplier_count
        self.product_count = product_count

        self.start_product_id = (
                start_product_id
            )

    def generate_brands(self):

        brands = []

        for brand_id in range(
            1,
            self.brand_count + 1
        ):

            brands.append(
                {
                    "brand_id": brand_id,
                    "brand_name": f"Brand_{brand_id}",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(brands)

    def generate_categories(self):

        categories = []

        for category_id in range(
            1,
            self.category_count + 1
        ):

            categories.append(
                {
                    "category_id": category_id,
                    "category_name": f"Category_{category_id}",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(categories)

    def generate_suppliers(self):

        suppliers = []

        for supplier_id in range(
            1,
            self.supplier_count + 1
        ):

            suppliers.append(
                {
                    "supplier_id": supplier_id,
                    "supplier_name": fake.company(),
                    "country": fake.country(),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(suppliers)

    def generate_products(self):

        products = []

        # for product_id in range(
        #     1,
        #     self.product_count + 1
        # ):
        for product_id in range(

            self.start_product_id,

            self.start_product_id
            + self.product_count

        ):

            products.append(
                {
                    "product_id": product_id,

                    "brand_id":
                    random.randint(
                        1,
                        self.brand_count
                    ),

                    "category_id":
                    random.randint(
                        1,
                        self.category_count
                    ),

                    "supplier_id":
                    random.randint(
                        1,
                        self.supplier_count
                    ),

                    "product_name":
                    fake.word().capitalize(),

                    "price":
                    round(
                        np.random.uniform(
                            100,
                            5000
                        ),
                        2
                    ),

                    "created_at":
                    datetime.now(),

                    "updated_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(products)

    def generate(self):

        return {

            "brands":
            self.generate_brands(),

            "categories":
            self.generate_categories(),

            "suppliers":
            self.generate_suppliers(),

            "products":
            self.generate_products()
        }