# Select image to use
FROM "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye"

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