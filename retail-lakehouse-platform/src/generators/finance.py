from faker import Faker
import pandas as pd
import random
from datetime import datetime

fake = Faker()


class FinanceGenerator:

    def __init__(
        self,
        orders_df,
        returns_df
    ):

        self.orders_df = orders_df
        self.returns_df = returns_df

    # ==========================
    # INVOICES
    # ==========================

    def generate_invoices(self):

        invoices = []

        for row in self.orders_df.itertuples():

            invoices.append(
                {
                    "invoice_id":
                    row.order_id,

                    "order_id":
                    row.order_id,

                    "invoice_amount":
                    row.total_amount,

                    "invoice_date":
                    row.order_date,

                    "created_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(invoices)

    # ==========================
    # TAX
    # ==========================

    def generate_tax(self):

        taxes = []

        for row in self.orders_df.itertuples():

            taxes.append(
                {
                    "tax_id":
                    row.order_id,

                    "order_id":
                    row.order_id,

                    "taxable_amount":
                    row.total_amount,

                    "tax_percentage":
                    18,

                    "tax_amount":
                    round(
                        row.total_amount * 0.18,
                        2
                    ),

                    "created_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(taxes)

    # ==========================
    # REFUNDS
    # ==========================

    def generate_refunds(self):

        refunds = []

        for row in self.returns_df.itertuples():

            refunds.append(
                {
                    "refund_id":
                    row.return_id,

                    "order_id":
                    row.order_id,

                    "refund_amount":
                    row.refund_amount,

                    "refund_date":
                    fake.date_time_this_year(),

                    "created_at":
                    datetime.now()
                }
            )

        return pd.DataFrame(refunds)

    # ==========================
    # LEDGER
    # ==========================

    def generate_ledger(self):

        ledger = []

        ledger_id = 1

        # Revenue Entries

        for row in self.orders_df.itertuples():

            ledger.append(
                {
                    "ledger_id":
                    ledger_id,

                    "order_id":
                    row.order_id,

                    "entry_type":
                    "REVENUE",

                    "amount":
                    row.total_amount,

                    "entry_timestamp":
                    datetime.now()
                }
            )

            ledger_id += 1

        # Refund Entries

        for row in self.returns_df.itertuples():

            ledger.append(
                {
                    "ledger_id":
                    ledger_id,

                    "order_id":
                    row.order_id,

                    "entry_type":
                    "REFUND",

                    "amount":
                    -row.refund_amount,

                    "entry_timestamp":
                    datetime.now()
                }
            )

            ledger_id += 1

        return pd.DataFrame(ledger)

    # ==========================
    # MAIN
    # ==========================

    def generate(self):

        return {

            "invoices":
            self.generate_invoices(),

            "refunds":
            self.generate_refunds(),

            "tax":
            self.generate_tax(),

            "ledger":
            self.generate_ledger()
        }