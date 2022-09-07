FROM apache/airflow:2.3.3
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
