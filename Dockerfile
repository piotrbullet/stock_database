FROM python:3.9.7

ADD ./docker/web_server/requirements.txt requirements.txt
RUN python3 -m pip  install -r requirements.txt
RUN pip install scipy

COPY ./ ./
