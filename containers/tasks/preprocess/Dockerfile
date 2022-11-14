FROM continuumio/miniconda3:4.12.0
RUN \
  apt-get update && \
  apt-get -y install vim curl git
RUN \
  conda install -c conda-forge rdkit
RUN git clone https://github.com/med-sci/checkmol.git
RUN pip install /k8s_mlops/mlbase
WORKDIR /k8s_mlops/containers/tasks/preprocess/
RUN pip install --no-cache-dir --upgrade -r requirements.txt