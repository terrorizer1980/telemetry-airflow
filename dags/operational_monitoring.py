from airflow import DAG
from datetime import timedelta, datetime
from utils.gcp import gke_command

default_args = {
    "owner": "msamuel@mozilla.com",
    "email": [
        "telemetry-alerts@mozilla.com",
        "msamuel@mozilla.com",
    ],
    "depends_on_past": False,
    "start_date": datetime(2021, 6, 3),
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 2,
    "retry_delay": timedelta(minutes=30),
}
PROJECT_ID="operational_monitoring"

with DAG(PROJECT_ID, default_args=default_args, schedule_interval="@daily") as dag:
    operational_monitoring = gke_command(
        task_id="run_operational_monitoring",
        command=[
            "bqetl",
            "opmon",
            "run",
            "--submission-date={{ ds }}",
        ],
        docker_image="mozilla/bigquery-etl:latest",
        dag=dag,
    )
