FROM python:slim

COPY ./lib/dm-interface-1.0.4.tar.gz /

RUN pip install psutil dm-interface-1.0.4.tar.gz ipfshttpclient

COPY ./src /src

WORKDIR /src