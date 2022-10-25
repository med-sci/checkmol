FROM python:3.10-slim-buster
WORKDIR /home/mlflow
COPY ./requirements.txt /home/mlflow/requirements.txt
RUN \
  apt-get update && \
  apt-get -y install vim curl git
RUN pip install --no-cache-dir --upgrade -r requirements.txt
EXPOSE 5000