# Select image to use
FROM python:3.12.4-slim

# Copy python requirements file
COPY ./scrapper/endi-scrapper/requirements.txt .

# Install python requirements and download spaCy model
RUN pip install -r requirements.txt --ignore-installed && \
    python -m spacy download es_core_news_sm

# Copy project folder to container volume
COPY ./scrapper/endi-scrapper/src src

# Execute service
CMD ["python", "/src/main.py"]