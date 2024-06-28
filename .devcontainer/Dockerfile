# Select image to use
FROM "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye"

# Variables to be used
ARG USERNAME=vscode
ARG USER_ID=1000
ARG USER_GID=$USER_ID

# Turn off prompt ask user for permissions
ENV DEBIAN_FRONTEND=noninteractive

# Update Linux
RUN apt-get -y update --no-install-recommends

# Upgrade Linux
RUN apt-get -y upgrade

# # Install pip
# # RUN apt-get install -y python3-pip

# # Update/upgrade pip
# RUN pip install --upgrade pip

# # Install requirements
# COPY requirements.txt ./
# RUN yes | pip install -r requirements.txt

# Remove dependencies no longer used 
RUN apt-get autoremove -y

# Clears local repo of retrieved package files
RUN apt-get clean -y

ENV DEBIAN_FRONTEND=dialog

# USER $USERNAME