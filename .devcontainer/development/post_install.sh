#!/bin/bash
# Update pip
pip install --upgrade pip

cd ./.devcontainer/development

# Install requirements
yes | pip install -r requirements.txt --ignore-installed