FROM python:3.10-slim-buster
RUN \
  apt-get update && \
  apt-get -y install git
RUN git clone https://github.com/med-sci/k8s_mlops.git
WORKDIR /k8s_mlops/containers/api
RUN pip install --no-cache-dir --upgrade -r requirements.txt