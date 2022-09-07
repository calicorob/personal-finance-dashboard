# personal-finance-dashboard
This repository hosts the files and instructions needed to get my personal finance dashboard up and running on any system. 

## Premise
A couple months ago I decided to start tracking my expenses. Originally, I started tracking my expenses in Google Sheets but soon became annoyed having to manually build the graphs for analyzing my expenses over time or by category.

I wanted something that was easy; put my numbers in a spreadsheet and forget about it.

So, I decided to use my data engineering skills and build a Google Sheets -> dashboard pipeline. With this, I would only have to:
1. Put my expenses into a Google Sheet.
2. Run the pipeline.
3. Enjoy the breakdown of my expenses in a dashboard.

## Setup
This project has 3 steps:
1. Expenses input in Google Sheets.
2. Data manipulation / pipeline via Apache Airflow.
3. Data visualization with Streamlit. 

### Google Sheets
To start, I put my expenses into a Google Sheet document. An example document will be linked here. 

Accessing the data in a Google Sheet can be done in multiple ways, official documentation [here](https://developers.google.com/sheets/api/quickstart/python).

I chose to go the service account route, so I created a service account and shared the Google Sheet file with that service account.

Having shared the Google Sheet document with the created service account, I can access the Google Sheet if I have the credentials to that service account. Credentials for the service account can be generated and put into a JSON file.

Information on authentication with a service account credentials through the google.oauth2 module can be found [here](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html). 

[Scripts](./dags/gsheet_api/core.py) for accessing the Google Sheets data were then built using this premise and put into the data pipeline. 

### Docker 
For this project, I have chosen to run Airflow off of Docker. I chose Docker as it's easy to port applications between different systems through Docker images and containers. 

Docker installation instructions for Ubuntu can be found [here](https://docs.docker.com/engine/install/ubuntu/). 
Installing Docker on other system, e.g. Windows / Mac is fairly straightfoward and specific instruction can be found with a quick google search.

### Airflow
Task orchestration & resulting data pipeline is accomplished through Airflow. 

Instructions for getting Airflow running in Docker can be found [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

The simplified instructions are:
1. Create mounted folders required for Airflow. The paths for the mounted folders can be found in lines 62-67 of the docker compose. 
2. Add service account credentials JSON to 'keys' folder as `service_key.json`. 
3. Set the AIRFLOW_UID.
4. Initialize database; docker-compose up airflow init.
5. Run; docker-compose up

### Visualization
Data visualization / dashboarding was done with streamlit. 

Installation instructions are as follows:

1. Create a virtual environment.
2. Install required libraries found in the [requirements.txt](./streamlit/requirements.txt) file in the newly created environment.
3. Run `python -m streamlit run main.py` in the [streamlit](./streamlit/) folder. 

### Next steps
* Expose dashboard online so I can access my finances anywhere. 
* Improve finances visualizations.