FROM python:3.9.7

ADD ./web_server/requirements.txt requirements.txt
COPY ./web_server/dashboard.py dashboard.py
COPY ./web_server/setup_psql_environment.py setup_psql_environment.py
COPY ./web_server/setup_psql_environment.yaml setup_psql_environment.yaml

RUN python3 -m pip  install -r requirements.txt
