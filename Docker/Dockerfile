FROM ubuntu:18.04


RUN \
apt-get update -qq && \
apt-get install -y \
build-essential \
apt-utils &&\
apt-get install -y \
curl \
sudo \
wget \
virtualenv \
unzip

RUN \
apt-get install -y \
python3.7 python3 python3-pip   &&\
pip3 install gevent && \
rm -rf /var/lib/apt/lists/*

ENV SHELL /bin/bash


WORKDIR /home/docker/crawler
