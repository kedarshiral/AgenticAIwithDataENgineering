from pathlib import Path
import pandas as pd
from datetime import datetime
import uuid


class AuditLogger:

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

        self.audit_file = (
            self.audit_dir
            / "audit_log.csv"
        )

    def log(
        self,
        table_name,
        row_count,
        file_format,
        storage_type,
        status="SUCCESS"
    ):

        record = {

            "run_id":
            str(
                uuid.uuid4()
            ),

            "table_name":
            table_name,

            "row_count":
            row_count,

            "file_format":
            file_format,

            "storage_type":
            storage_type,

            "load_timestamp":
            datetime.now(),

            "status":
            status
        }

        df = pd.DataFrame(
            [record]
        )

        if self.audit_file.exists():

            df.to_csv(
                self.audit_file,
                mode="a",
                header=False,
                index=False
            )

        else:

            df.to_csv(
                self.audit_file,
                index=False
            )