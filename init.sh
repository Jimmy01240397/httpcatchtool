#!/bin/bash


sudo apt install python3-venv 
python3 -m venv venv
. ./venv/bin/activate
python -m pip install wheel
python -m pip install -r requirements.txt

