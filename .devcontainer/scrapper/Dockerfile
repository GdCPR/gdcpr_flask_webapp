# Select image to use
FROM python:3.9.19-slim-bullseye

WORKDIR endi_scrapper

# Turn off prompt ask user for permissions
ENV DEBIAN_FRONTEND=noninteractive

# Update Linux
RUN apt-get -y update --no-install-recommends

# Upgrade Linux
RUN apt-get -y upgrade

# Remove dependencies no longer used 
RUN apt-get autoremove -y

# Clears local repo of retrieved package files
RUN apt-get clean -y

ENV DEBIAN_FRONTEND=dialog

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY scrapper .

CMD ["python", "/scrapper/main.py"]