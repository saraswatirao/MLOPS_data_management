from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.sensors.s3_key_sensor import S3KeySensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from preprocessing import preprocess_data
import os
from config import BUCKET_NAME, S3_FILE_PATH, PREPROCESSED_FILE_NAME, RAW_FILE_NAME, LOCAL_REPO_PATH
from s3_download import download_file_from_s3

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'max_active_runs': 1,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

dag = DAG(
    'data-pipeline-example',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False
)

# Task 1: S3 Sensor
check_if_data_file_arrived = S3KeySensor(
    task_id='check_if_data_file_arrived',
    poke_interval=10,  # Check for file every 60 seconds
    timeout=6000,  # Timeout if file not found after 600 seconds
    bucket_key=S3_FILE_PATH,  # Update with your S3 path
    bucket_name=BUCKET_NAME,
    mode='poke',
    dag=dag,
)

# Task 2: Download the file locally
download_file = PythonOperator(
    task_id="download_file",
    python_callable=download_file_from_s3,
    op_kwargs={"access_key": os.environ["AWS_ACCESS_KEY_ID"], "secret_key": os.environ["AWS_SECRET_ACCESS_KEY"], "bucket_name": BUCKET_NAME, "file_name": S3_FILE_PATH, "local_file_path": os.path.join(LOCAL_REPO_PATH, RAW_FILE_NAME)},
    provide_context=True,
    dag=dag
)

# Task 3: Python Operator for Preprocessing
preprocess_task = PythonOperator(
    task_id='preprocess_task',
    python_callable=preprocess_data,
    op_kwargs={"input_path": os.path.join(LOCAL_REPO_PATH, RAW_FILE_NAME), "output_path": os.path.join(LOCAL_REPO_PATH, PREPROCESSED_FILE_NAME)},
    provide_context=True,
    dag=dag,
)

# Task 4: Bash Operator for DVC Commands
dvc_commands_task = BashOperator(
    task_id='dvc_commands_task',
    bash_command='cd /opt/airflow/data-versioning-demo && dvc add *.csv && dvc commit -f && dvc push',
    dag=dag,
)

# Define Task Dependencies
check_if_data_file_arrived >> download_file >> preprocess_task >> dvc_commands_task
