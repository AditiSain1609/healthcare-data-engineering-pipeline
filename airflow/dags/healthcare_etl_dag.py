from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "healthcare-data-engineering",
    "depends_on_past": False,
    "retries": 1,
}


with DAG(
    dag_id="healthcare_etl_pipeline",
    default_args=default_args,
    description="End-to-end healthcare data engineering ETL pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["healthcare", "etl", "python", "mysql"],
) as dag:

    run_healthcare_pipeline = BashOperator(
        task_id="run_healthcare_pipeline",
        bash_command=(
            "cd /opt/airflow/project && "
            "python -m src.main"
        ),
    )


    run_healthcare_pipeline
    