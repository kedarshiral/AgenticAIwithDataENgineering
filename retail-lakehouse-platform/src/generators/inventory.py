from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()


class InventoryGenerator:

    def __init__(
        self,
        product_count=1000,
        warehouse_count=10,
        inventory_count=1000,
        movement_count=10000
    ):

        self.product_count = product_count
        self.warehouse_count = warehouse_count
        self.inventory_count = inventory_count
        self.movement_count = movement_count

    def generate_warehouses(self):

        warehouses = []

        for warehouse_id in range(
            1,
            self.warehouse_count + 1
        ):

            warehouses.append(
                {
                    "warehouse_id": warehouse_id,
                    "warehouse_name": f"WH_{warehouse_id}",
                    "city": fake.city(),
                    "state": fake.state(),
                    "created_at": datetime.now()
                }
            )

        return pd.DataFrame(warehouses)

    def generate_inventory(self):

        inventory = []

        for inventory_id in range(
            1,
            self.inventory_count + 1
        ):

            inventory.append(
                {
                    "inventory_id": inventory_id,
                    "warehouse_id": random.randint(
                        1,
                        self.warehouse_count
                    ),
                    "product_id": random.randint(
                        1,
                        self.product_count
                    ),
                    "quantity": random.randint(
                        0,
                        500
                    ),
                    "created_at": datetime.now()
                }
            )

        return pd.DataFrame(inventory)

    def generate_stock_movements(self):

        movements = []

        movement_types = [
            "INBOUND",
            "OUTBOUND",
            "ADJUSTMENT"
        ]

        for movement_id in range(
            1,
            self.movement_count + 1
        ):

            movements.append(
                {
                    "movement_id": movement_id,
                    "product_id": random.randint(
                        1,
                        self.product_count
                    ),
                    "warehouse_id": random.randint(
                        1,
                        self.warehouse_count
                    ),
                    "movement_type": random.choice(
                        movement_types
                    ),
                    "quantity": random.randint(
                        1,
                        100
                    ),
                    "movement_timestamp":
                    fake.date_time_this_year()
                }
            )

        return pd.DataFrame(movements)

    def generate(self):

        return {

            "warehouses":
            self.generate_warehouses(),

            "inventory":
            self.generate_inventory(),

            "stock_movements":
            self.generate_stock_movements()
        }