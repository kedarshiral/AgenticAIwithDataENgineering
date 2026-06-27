# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from airflow.operators.empty import EmptyOperator
# from airflow.operators.python import BranchPythonOperator
# from datetime import datetime
# from common_utils import dq_decision

# time = datetime.now()

# with DAG(
#     dag_id="retail_pipeline",
#     start_date=datetime(2025, 1, 1),
#     schedule=None,
#     catchup=False,
#     tags=["retail"]
# ) as dag:

#     generate_data = BashOperator(
#         task_id="generate_data",
#         bash_command="""
#         cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#         python -m scripts.run_generation
#         """
#     )

#     run_dq = BashOperator(
#         task_id="run_dq",
#         bash_command="""
#         cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#         python -m scripts.run_dq
#         """
#     )   

#     dq_branch = BranchPythonOperator(
#     task_id="dq_decision",
#     python_callable=dq_decision
#     )

#     dq_success_handler = EmptyOperator(
#         task_id="dq_success_handler"
#     )

#     dq_failure_handler = EmptyOperator(
#         task_id="dq_failure_handler"
#     )

#     push_to_github = BashOperator(
#         task_id="push_to_github",
#         bash_command=f"""
#             cd /opt/AgenticAIwithDataENgineering

#             git add .

#             git commit -m "Auto refresh {time}"

#             git push
#             """
#     )

#     github_fetch = BashOperator(
#     task_id="github_fetch",
#     bash_command="""
#     cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#     python -m src.ingestion.github_fetcher
#     """
# )
#     landing_loader = BashOperator(
#     task_id="landing_loader",
#     bash_command="""
#     cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#     python -m src.ingestion.landing_loader
#     """
# )
    
#     raw_loader = BashOperator(
#     task_id="raw_loader",
#     bash_command="""
#     cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#     python -m src.ingestion.raw_loader
#     """
# )
    
#     l0_to_l1 = BashOperator(
#     task_id="l0_to_l1",
#     bash_command="""
#     cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#     python -m scripts.run_l0_to_l1
#     """
# )
    
#     l1_to_l2 = BashOperator(
#     task_id="l1_to_l2",
#     bash_command="""
#     cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#     python -m scripts.run_l1_to_l2
#     """
# )
    
#     l2_to_l3 = BashOperator(
#     task_id="l2_to_l3",
#     bash_command="""
#     cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
#     python -m scripts.run_l2_to_l3
#     """
# )
    
#     metadata_refresh = EmptyOperator(
#     task_id="metadata_refresh"
# )

# generate_data >> run_dq >> dq_branch

# dq_branch >> dq_success_handler >> push_to_github

# dq_branch >> dq_failure_handler

# push_to_github >> github_fetch

# github_fetch >> landing_loader

# landing_loader >> raw_loader

# raw_loader >> l0_to_l1

# l0_to_l1 >> l1_to_l2

# l1_to_l2 >> l2_to_l3

# l2_to_l3 >> metadata_refresh

from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator

from common_utils import dq_decision


time = datetime.now()


with DAG(
    dag_id="retail_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["retail", "lakehouse", "agentic-ai"]
) as dag:

    # ==========================================================
    # DATA GENERATION
    # ==========================================================

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.run_generation
        """
    )

    # ==========================================================
    # PUSH TO GITHUB (API SIMULATION)
    # ==========================================================

    push_to_github = BashOperator(
        task_id="push_to_github",
        bash_command=f"""
        cd /opt/AgenticAIwithDataENgineering

        git add .

        git commit -m "Auto refresh {time}"

        git push
        """
    )

    # ==========================================================
    # FETCH FROM GITHUB
    # ==========================================================

    github_fetch = BashOperator(
        task_id="github_fetch",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m src.ingestion.github_fetcher
        """
    )

    # ==========================================================
    # LANDING
    # ==========================================================

    landing_loader = BashOperator(
        task_id="landing_loader",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m src.ingestion.landing_loader
        """
    )

    # ==========================================================
    # RAW
    # ==========================================================

    raw_loader = BashOperator(
        task_id="raw_loader",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m src.ingestion.raw_loader
        """
    )

    # ==========================================================
    # DQ
    # ==========================================================

    run_dq = BashOperator(
        task_id="run_dq",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.run_dq
        """
    )

    dq_branch = BranchPythonOperator(
        task_id="dq_decision",
        python_callable=dq_decision
    )

    dq_success_handler = EmptyOperator(
        task_id="dq_success_handler"
    )

    dq_failure_handler = EmptyOperator(
        task_id="dq_failure_handler"
    )

    # ==========================================================
    # L0 → L1
    # ==========================================================

    l0_to_l1 = BashOperator(
        task_id="l0_to_l1",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.run_l0_to_l1
        """
    )

    # ==========================================================
    # L1 → L2
    # ==========================================================

    l1_to_l2 = BashOperator(
        task_id="l1_to_l2",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.run_l1_to_l2
        """
    )

    # ==========================================================
    # L2 → L3
    # ==========================================================

    l2_to_l3 = BashOperator(
        task_id="l2_to_l3",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.run_l2_to_l3
        """
    )

    # ==========================================================
    # METADATA
    # ==========================================================

    metadata_refresh = BashOperator(
        task_id="metadata_refresh",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.run_metadata_refresh
        """
    )

    # ==========================================================
    # LINEAGE
    # ==========================================================

    lineage_refresh = BashOperator(
        task_id="lineage_refresh",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.build_lineage_catalog
        """
    )

    # ==========================================================
    # DATA DICTIONARY
    # ==========================================================

    data_dictionary_refresh = BashOperator(
        task_id="data_dictionary_refresh",
        bash_command="""
        cd /opt/AgenticAIwithDataENgineering/retail-lakehouse-platform &&
        python -m scripts.build_data_dictionary
        """
    )

    # ==========================================================
    # PIPELINE SUCCESS
    # ==========================================================

    pipeline_success = EmptyOperator(
        task_id="pipeline_success"
    )

    # ==========================================================
    # FUTURE AI AGENTS (PLACEHOLDERS)
    # ==========================================================

    # rca_agent
    # schema_drift_agent
    # impact_analysis_agent
    # notification_agent
    # approval_agent
    # chat_agent

    # ==========================================================
    # DAG FLOW
    # ==========================================================

    generate_data >> push_to_github

    push_to_github >> github_fetch

    github_fetch >> landing_loader

    landing_loader >> raw_loader

    raw_loader >> run_dq

    run_dq >> dq_branch

    dq_branch >> dq_success_handler

    dq_branch >> dq_failure_handler

    dq_success_handler >> l0_to_l1

    l0_to_l1 >> l1_to_l2

    l1_to_l2 >> l2_to_l3

    l2_to_l3 >> metadata_refresh

    metadata_refresh >> lineage_refresh

    lineage_refresh >> data_dictionary_refresh

    data_dictionary_refresh >> pipeline_success