FROM conda/miniconda3

RUN apt-get update && apt-get -y install gcc && apt-get install -y g++

RUN conda install pdal python-pdal gdal -c conda-forge && pip install --upgrade pip && pip install laserfarm --ignore-installed certifi

RUN pip install psutil dm-interface

# docker build -t nicoja/ecolidar .