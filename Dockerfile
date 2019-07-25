FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

RUN apt-get update
RUN apt install -y python-pip

COPY src /root/src
WORKDIR /root/src
RUN pip install -r requirements.txt