
from pathlib import Path
import gsheet_api.api as api
import csv 
import os


# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

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


if __name__ == '__main__':
    dump_csvs()