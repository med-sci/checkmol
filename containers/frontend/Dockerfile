FROM node:19.1-buster-slim
RUN \
  apt-get update && \
  apt-get -y install git
RUN git clone https://github.com/med-sci/checkmol.git
# RUN pip install /checkmol/mlbase
WORKDIR /checkmol/containers/frontend
RUN npm ci