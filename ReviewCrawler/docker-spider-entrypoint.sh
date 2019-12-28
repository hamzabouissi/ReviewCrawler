#!/bin/bash

if [ ! -e env ]
then
  virtualenv env --python=python3.7
fi
source ./env/bin/activate
ls la
pip install -r requirements.txt

scrapy crawl bookingSpi 
