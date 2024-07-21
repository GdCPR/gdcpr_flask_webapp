#!/bin/bash
# Update pip
pip install --upgrade pip

# Change to root dir
cd .

# Install requirements
yes | pip install -r requirements.txt --ignore-installed