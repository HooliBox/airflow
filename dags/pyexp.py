from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pprint import pprint
import requests
import logging
import cx_Oracle 
from airflow.exceptions import AirflowException

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 28, 22, 15),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}


dag = DAG('pythonexp', default_args=default_args, schedule_interval=timedelta(days=1))


def pushing_task(ds, **kwargs):
    return 10000


def pull_function(**context):
    value = context['task_instance'].xcom_pull(task_ids='pushing_task')
    print(value)


t1 = PythonOperator(
    task_id='pushing_task',
    provide_context=True,
    python_callable=pushing_task,
    dag=dag,
)

t2 = PythonOperator(
    task_id='pull_task', 
    python_callable=pull_function,
    provide_context=True,
    dag=dag)


t1 >> t2
