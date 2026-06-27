from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()


class MarketingGenerator:

    def __init__(
        self,
        customer_count=5000,
        campaign_count=50,
        impression_count=100000,
        click_count=25000,
        email_event_count=25000,
        start_campaign_id=1
    ):

        self.customer_count = customer_count
        self.campaign_count = campaign_count
        self.impression_count = impression_count
        self.click_count = click_count
        self.email_event_count = email_event_count

        self.start_campaign_id = (
            start_campaign_id
        )

    # =========================
    # CAMPAIGNS
    # =========================

    def generate_campaigns(self):

        campaigns = []

        # for campaign_id in range(
        #     1,
        #     self.campaign_count + 1
        # ):
        for campaign_id in range(

            self.start_campaign_id,

            self.start_campaign_id
            + self.campaign_count

        ):

            start_date = fake.date_between(
                start_date="-1y",
                end_date="today"
            )

            campaigns.append(
                {
                    "campaign_id":
                    campaign_id,
                    "campaign_name": f"Campaign_{campaign_id}",
                    "channel": random.choice(
                        [
                            "Email",
                            "Facebook",
                            "Google",
                            "Instagram"
                        ]
                    ),
                    "budget": random.randint(
                        10000,
                        500000
                    ),
                    "start_date": start_date,
                    "end_date": start_date + timedelta(days=30),
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
            )

        return pd.DataFrame(campaigns)

    # =========================
    # IMPRESSIONS
    # =========================

    def generate_impressions(self):

        impressions = []

        for impression_id in range(
            1,
            self.impression_count + 1
        ):

            impressions.append(
                {
                    "impression_id": impression_id,
                    "campaign_id":
                    random.randint(
                        self.start_campaign_id,
                        self.start_campaign_id
                        + self.campaign_count
                        - 1
                    ),
                    "customer_id":
                    random.randint(

                        self.customer_count - 49,

                        self.customer_count

                    ),
                    "impression_timestamp":
                    fake.date_time_this_year(),
                    "created_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(impressions)

    # =========================
    # CLICKS
    # =========================

    def generate_clicks(self):

        clicks = []

        for click_id in range(
            1,
            self.click_count + 1
        ):

            clicks.append(
                {
                    "click_id": click_id,
                    "campaign_id":
                    random.randint(
                        self.start_campaign_id,
                        self.start_campaign_id
                        + self.campaign_count
                        - 1
                    ),
                    "customer_id":
                    random.randint(

                        self.customer_count - 49,

                        self.customer_count

                    ),
                    "click_timestamp":
                    fake.date_time_this_year(),
                    "created_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(clicks)

    # =========================
    # EMAIL EVENTS
    # =========================

    def generate_email_events(self):

        email_events = []

        event_types = [
            "SENT",
            "OPENED",
            "CLICKED",
            "BOUNCED"
        ]

        for event_id in range(
            1,
            self.email_event_count + 1
        ):

            email_events.append(
                {
                    "event_id": event_id,
                    "campaign_id":
                    random.randint(
                        self.start_campaign_id,
                        self.start_campaign_id
                        + self.campaign_count
                        - 1
                    ),
                    "customer_id":
                    random.randint(

                        self.customer_count - 49,

                        self.customer_count

                    ),
                    "event_type": random.choice(
                        event_types
                    ),
                    "event_timestamp":
                    fake.date_time_this_year(),
                    "created_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(email_events)

    # =========================
    # MAIN
    # =========================

    def generate(self):

        return {

            "campaigns":
            self.generate_campaigns(),

            "impressions":
            self.generate_impressions(),

            "clicks":
            self.generate_clicks(),

            "email_events":
            self.generate_email_events()
        }