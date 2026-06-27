from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()


# class CustomerGenerator:

#     def __init__(self, customer_count=5000):

#         self.customer_count = customer_count

class CustomerGenerator:

    def __init__(
        self,
        customer_count=50,
        start_customer_id=1
    ):

        self.customer_count = customer_count

        self.start_customer_id = (
            start_customer_id
        )

    def generate_customers(self):

        customers = []

        # for customer_id in range(
        #     1,
        #     self.customer_count + 1
        # ):

        for customer_id in range(

            self.start_customer_id,

            self.start_customer_id
            + self.customer_count

        ):

            customers.append(
                {
                    "customer_id": customer_id,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "email": fake.email(),
                    "phone": fake.phone_number(),
                    "registration_date": fake.date_between(
                        start_date="-3y",
                        end_date="today"
                    ),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(customers)

    def generate_customer_addresses(self):

        addresses = []

        for idx, customer_id in enumerate(

            range(

                self.start_customer_id,

                self.start_customer_id
                + self.customer_count

            ),

            start=1

        ):

            addresses.append(
                {
                    "address_id": customer_id,
                    "customer_id": customer_id,
                    "address_line": fake.street_address(),
                    "city": fake.city(),
                    "state": fake.state(),
                    "country": fake.country(),
                    "zip_code": fake.postcode(),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(addresses)

    def generate_customer_segments(self):

        segments = []

        segment_choices = [
            "Bronze",
            "Silver",
            "Gold",
            "Platinum"
        ]

        for customer_id in range(

            self.start_customer_id,

            self.start_customer_id
            + self.customer_count

        ):

            segments.append(
                {
                    "segment_id": customer_id,
                    "customer_id": customer_id,
                    "segment_name": random.choice(
                        segment_choices
                    ),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(segments)

    def generate(self):

        return {
            "customers":
                self.generate_customers(),

            "customer_addresses":
                self.generate_customer_addresses(),

            "customer_segments":
                self.generate_customer_segments()
        }