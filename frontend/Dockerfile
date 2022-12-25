FROM node:19.1-buster-slim
RUN \
  apt-get update && \
  apt-get -y install git
RUN git clone https://github.com/med-sci/checkmol.git
WORKDIR /checkmol/frontend
RUN npm ci