FROM python:3.10-slim-buster
WORKDIR /home/train
COPY ./requirements.txt /home/train/requirements.txt
COPY ./train.py /home/train/train.py
RUN \
  apt-get update && \
  apt-get -y install vim curl git
RUN pip install --no-cache-dir --upgrade -r requirements.txt
