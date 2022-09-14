FROM python:3.9.7

ADD ./requirements.txt requirements.txt
RUN python3 -m pip  install -r requirements.txt

COPY ./dashboard.py dashboard.py
COPY ./setup_psql_environment.py setup_psql_environment.py
COPY ./setup_psql_environment.yaml setup_psql_environment.yaml
