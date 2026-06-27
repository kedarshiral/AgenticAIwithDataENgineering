from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()


class OrderGenerator:

    def __init__(
        self,
        customer_count=5050,
        product_count=1005,
        campaign_count=52,
        order_count=100,
        start_order_id=1,
        start_order_item_id=1,
        start_campaign_id=1

    ):

        self.customer_count = customer_count
        self.product_count = product_count
        self.campaign_count = campaign_count
        self.order_count = order_count

        self.start_order_id = (
            start_order_id
        )

        self.start_order_item_id = (
            start_order_item_id
        )

        self.start_campaign_id = (
            start_campaign_id
        )

    def generate_orders(
                    self,
                    order_totals
                ):

        orders = []

        for order_id in range(

            self.start_order_id,

            self.start_order_id
            + self.order_count

        ):

            orders.append(
                {
                    "order_id": order_id,
                    "customer_id":
                    random.randint(

                        self.customer_count - 49,

                        self.customer_count

                    ),
                    "campaign_id":
                    random.randint(

                        self.start_campaign_id,

                        self.start_campaign_id
                        + self.campaign_count
                        - 1

                    ),
                    "order_date":
                    fake.date_time_this_year(),
                    "order_status":
                    random.choice(
                        [
                            "PLACED",
                            "SHIPPED",
                            "DELIVERED"
                        ]
                    ),
                    # "total_amount":
                    # round(
                    #     random.uniform(
                    #         100,
                    #         10000
                    #     ),
                    #     2
                    "total_amount":
                        order_totals[
                            order_id
                        ]
                }
            )

        return pd.DataFrame(orders)

    def generate_order_items(self):

        items = []

        order_totals = {}

        order_item_id = (
            self.start_order_item_id
        )

        # for order_id in range(
        #     1,
        #     self.order_count + 1
        # ):
        for order_id in range(

            self.start_order_id,

            self.start_order_id
            + self.order_count

        ):

            total_amount = 0

            item_count = random.randint(
                1,
                5
            )

            for _ in range(item_count):

                quantity = random.randint(
                    1,
                    5
                )

                unit_price = round(
                    random.uniform(
                        100,
                        5000
                    ),
                    2
                )

                line_amount = round(
                    quantity * unit_price,
                    2
                )

                total_amount += line_amount

                items.append(
                    {
                        "order_item_id":
                        order_item_id,

                        "order_id":
                        order_id,

                        "product_id":
                        random.randint(

                            self.product_count - 4,

                            self.product_count

                        ),

                        "quantity":
                        quantity,

                        "unit_price":
                        unit_price,

                        "line_amount":
                        line_amount
                    }
                )

                order_item_id += 1

            order_totals[
                order_id
            ] = round(
                total_amount,
                2
            )

        return (
            pd.DataFrame(items),
            order_totals
        )

    def generate_payments(
    self,
    orders_df
):

        payments = []

        for row in orders_df.itertuples():

            status = random.choices(
                ["SUCCESS", "FAILED"],
                weights=[95, 5]
            )[0]

            payments.append(
                {
                    "payment_id":
                    row.order_id,

                    "order_id":
                    row.order_id,

                    "payment_method":
                    random.choice(
                        [
                            "CARD",
                            "UPI",
                            "NETBANKING",
                            "COD"
                        ]
                    ),

                    "payment_status":
                    status,

                    "payment_amount":
                    row.total_amount
                    if status == "SUCCESS"
                    else 0
                }
            )

        return pd.DataFrame(payments)

    def generate_returns(
    self,
    orders_df
):
        delivered_orders = (
                orders_df[
                    orders_df["order_status"]
                    == "DELIVERED"
                ]
                )

        returns = []

        return_id = 1

        for row in delivered_orders.itertuples():

            if random.random() < 0.05:

                returns.append(
                    {
                        "return_id":
                        return_id,

                        "order_id":
                        row.order_id,

                        # "refund_amount":
                        # round(
                        #     random.uniform(
                        #         100,
                        #         5000
                        #     ),
                        #     2
                        # ),
                        "refund_amount":
                            round(
                                random.uniform(
                                    row.total_amount * 0.3,
                                    row.total_amount
                                ),
                                2
                            ),

                        "return_reason":
                        random.choice(
                            [
                                "DAMAGED",
                                "WRONG_PRODUCT",
                                "CUSTOMER_CANCELLED"
                            ]
                        )
                    }
                )

                return_id += 1

        return pd.DataFrame(returns)

    def generate(self):

        items_df, order_totals = (
            self.generate_order_items()
        )

        orders_df = (
            self.generate_orders(
                order_totals
            )
        )

        payments_df = (
            self.generate_payments(
                orders_df
            )
        )

        # returns_df = (
        #     self.generate_returns()
        # )

        returns_df = (
                self.generate_returns(
                    orders_df
                )
            )

        return {

            "orders":
            orders_df,

            "order_items":
            items_df,

            "payments":
            payments_df,

            "returns":
            returns_df
        }