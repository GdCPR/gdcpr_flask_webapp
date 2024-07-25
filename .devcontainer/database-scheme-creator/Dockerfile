# Select image to use
FROM python:3.12.4-slim-bullseye

# Turn off prompt ask user for permissions
ENV DEBIAN_FRONTEND=noninteractive

# Update Linux
RUN apt-get -y update --no-install-recommends

# Install build essentials
RUN apt-get -y install build-essential

# RUN apt-get -y install gcc

# RUN apt-get -y install python-devel libxslt-devel libffi-devel openssl-devel

# Upgrade Linux
RUN apt-get -y upgrade

# Remove dependencies no longer used 
RUN apt-get autoremove -y

# Clears local repo of retrieved package files
RUN apt-get clean -y

ENV DEBIAN_FRONTEND=dialog

COPY ./database-scheme-creator/requirements.txt .

RUN pip install --upgrade pip

RUN pip install --upgrade setuptools

RUN pip install -r requirements.txt --ignore-installed

COPY ./database-scheme-creator/scrapper scrapper

CMD ["python", "/scrapper/database_manager/clean_setup.py"]