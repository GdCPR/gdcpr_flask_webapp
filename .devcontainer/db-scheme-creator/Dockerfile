# Select image to use
FROM python:3.12.4-slim-bullseye

# Turn off prompt ask user for permissions
ENV DEBIAN_FRONTEND=noninteractive

# Update Linux
RUN apt-get -y update --no-install-recommends

# Install build essentials
RUN apt-get -y install build-essential

# Upgrade Linux
RUN apt-get -y upgrade

# Remove dependencies no longer used 
RUN apt-get autoremove -y

# Clears local repo of retrieved package files
RUN apt-get clean -y

# Turn on prompt ask user for permissions
ENV DEBIAN_FRONTEND=dialog

# Copy python requirements file to container
COPY ./db-scheme-creator/requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install setupstools
RUN pip install --upgrade setuptools

# Install python requirements
RUN pip install -r requirements.txt --ignore-installed

# Copy database manager to container
COPY ./db-scheme-creator/db_manager db_manager

# Run python script to create clean db scheme
CMD ["python", "/db_manager/clean_setup.py"]