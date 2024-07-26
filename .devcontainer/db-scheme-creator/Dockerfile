# Select image to use
FROM python:3.12.4-alpine3.20

# Copy python requirements file to container
COPY ./db-scheme-creator/requirements.txt .

RUN pip install -r requirements.txt --ignore-installed

# Copy database manager to container
COPY ./db-scheme-creator/db_manager db_manager

# Run python script to create clean db scheme
CMD ["python", "/db_manager/clean_setup.py"]