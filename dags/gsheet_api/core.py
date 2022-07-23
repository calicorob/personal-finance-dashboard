from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from typing import  Optional, List

# gsheet credentials

__all__ = ["get_gsheet_array"]

def get_gsheet_credentials(filename:Optional[str] = None, scopes:Optional[List[str]] = None):
    
    # service account credentials
    if filename is None:
        filename = os.environ.get('gsheet_service_key')
        if filename is None:
            raise ValueError('Service account JSON credential not found. Please create an environment variable titled "g_sheet_service_key" with the path to your service account credentials.')
    # scope
    if scopes is None:
        scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']


    # gsheet credentials
    return service_account.Credentials.from_service_account_file(filename=filename, scopes=scopes)


def get_gsheet_array(spreadsheet_id:str,sheet_name:str,range_start:str,range_end:str,**kwargs)->Optional[List[List[str]]]:
    range_name = "".join([sheet_name,'!',range_start,':',range_end])
    
    creds = get_gsheet_credentials(**kwargs)
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range_name).execute()
    values = result.get('values')

    return values


def main()->None:
    pass  




if __name__ == '__main__':
    main()

