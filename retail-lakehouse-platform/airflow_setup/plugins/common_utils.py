import pandas as pd

def dq_decision():

    import pandas as pd

    df = pd.read_csv(
        "/opt/AgenticAIwithDataENgineering/retail-lakehouse-platform/audit/dq_results.csv"
    )

    fail_count = len(
        df[
            df["status"] == "FAIL"
        ]
    )

    if fail_count > 0:
        return "dq_failure_handler"

    return "dq_success_handler"
