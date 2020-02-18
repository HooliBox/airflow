from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pandas import DataFrame
import pandas as pd
from custom.dataframe_to_postgres_operator import PostgresOperatorBulk
from airflow.operators.postgres_operator import PostgresOperator

def read_df(task_instance, **context):
    df = pd.read_parquet('/usr/local/airflow/data/df.parquet.gzip')
    print(df)
    task_instance.__dict__['data'] = df

    return df

def get_df(task_instance, **context):
    for k, v in context.items():
        print(k, v)
    df =  task_instance.__dict__['data']
    print(df)


default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 2, 17),
    'retries': 0,
}

dag = DAG('abcdefg', default_args=default_args, schedule_interval=timedelta(days=1))

task_read_df = PythonOperator(
    task_id='read_df',
    python_callable=read_df,
    dag=dag,
    provide_context=True,
    do_xcom_push=False
)

task_get_df = PythonOperator(
    task_id='get_df',
    python_callable=get_df,
    dag=dag,
    provide_context=True,
    do_xcom_push=False
)

task_read_df >> task_get_df