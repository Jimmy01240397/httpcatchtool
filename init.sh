#!/bin/bash


sudo apt install python3-venv 
. ./venv/bin/activate
python -m venv venv
python -m pip install wheel
python -m pip install -r requirements.txt

