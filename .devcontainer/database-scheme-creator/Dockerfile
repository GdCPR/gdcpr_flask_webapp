# Select image to use
FROM python:3.12.4-alpine3.20

# Copy python requirements file to container
COPY ./database-scheme-creator/requirements.txt .

RUN pip install -r requirements.txt --ignore-installed

# Copy database manager to container
COPY ./database-scheme-creator/database_manager database_manager

# Run python script to create clean db scheme
CMD ["python", "/database_manager/clean_setup.py"]