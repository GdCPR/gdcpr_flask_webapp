# Select image to use
FROM "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye"

# Turn off prompt ask user for permissions
ENV DEBIAN_FRONTEND=noninteractive

# Update Linux
RUN apt-get -y update --no-install-recommends && \
    apt-get -y upgrade && \
    apt-get autoremove -y && \
    apt-get clean -y

# Turn on prompt ask user for permissions
ENV DEBIAN_FRONTEND=dialog