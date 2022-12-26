FROM continuumio/miniconda3:4.12.0
RUN \
  apt-get update && \
  apt-get -y install git
RUN \
  conda install -c conda-forge rdkit
RUN git clone https://github.com/med-sci/checkmol.git
RUN pip install /checkmol/mlbase
WORKDIR /checkmol/api
RUN pip install --no-cache-dir --upgrade -r requirements.txt