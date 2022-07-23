# library imports

import pendulum
from datetime import timedelta

from typing import Optional

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
import gsheet_api.api as api

from pathlib import Path
import os
import csv


# dag parameters
service_key_path = Path(os.getcwd())/'keys'/'service_key.json'
csv_folder = Path('./csvs')
spreadsheet_id = '1ELWxaWUkyuOfwUZe7tMLFF6PoViZ3UZ7ADlVd4WKRX4'
range_start = 'A1'
range_end = 'F'

sheet_names = [

     'Transportation'
    ,'Daily Living'
    ,'Entertainment'
    ,'Subscriptions'
    ,'Home Expenses'
    ,'Health'
    ,'Savings'
    ,'Misc'
    ,'Obligations'
    ,'Charity And Gifts'
]

def dump_csvs()->None:
    csv_folder.mkdir(exist_ok=True)

    for sheet_name in sheet_names:
        array = api.get_gsheet_array(spreadsheet_id=spreadsheet_id,sheet_name=sheet_name,range_start=range_start,range_end=range_end,filename = str(service_key_path))
        csv_path = csv_folder/"".join([sheet_name,'.csv'])

        with open(csv_path,mode='w',newline='') as file:
            wr = csv.writer(file,delimiter=',')
            wr.writerows(array)


    return 

    
# dag parameters
dag_id = 'dump_csvs'

default_args = {
     'owner':'robert.art.currie@gmail.com'
    ,'start_date':pendulum.datetime(year=2022,month=7,day=23)
    ,'retries':1
    ,'retry_delay':timedelta(seconds=10)
    ,'params':{}
}


with DAG(
     dag_id = dag_id
    ,default_args=default_args
    ,description = "Dump CSVs from google sheets."
    ,schedule_interval= None
) as dag:
    dag.doc_md = __doc__


    start = DummyOperator(task_id = 'start')
    dump_csvs = PythonOperator(task_id = 'dump_csvs',python_callable=dump_csvs)
    end = DummyOperator(task_id = 'end')


start >> dump_csvs >>  end 






