# Select image to use
FROM python:3.12.4-alpine3.20

# FROM python:3.12.4-slim-bullseye

# # Turn off prompt ask user for permissions
# ENV DEBIAN_FRONTEND=noninteractive
# # Update Linux, install essentials
# RUN apt -y update --no-install-recommends && \
#     # Upgrade Linux
#     apt -y upgrade --without-new-pkgs && \
#     # Remove dependencies no longer used 
#     apt -y autoremove --purge && \
#     # Clears local repo of retrieved package files
#     apt -y clean
# # Turn on prompt ask user for permissions
# ENV DEBIAN_FRONTEND=dialog

# Copy python requirements file to container
COPY ./db-scheme-creator/requirements.txt .

# # Upgrade pip
# RUN pip install --upgrade pip && \
#     # Install python requirements
#     pip install -r requirements.txt --ignore-installed

RUN pip install -r requirements.txt --ignore-installed

# Copy database manager to container
COPY ./db-scheme-creator/db_manager db_manager

# Run python script to create clean db scheme
CMD ["python", "/db_manager/clean_setup.py"]