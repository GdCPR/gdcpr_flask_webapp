# Select image to use
FROM python:3.12.4-slim

COPY ./scrapper/requirements.txt .

RUN pip install -r requirements.txt --ignore-installed && \
    python -m spacy download es_core_news_sm

COPY ./scrapper/scrapper scrapper

CMD ["python", "/scrapper/main.py"]