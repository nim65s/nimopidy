FROM python:latest

RUN mkdir /app
WORKDIR /app

COPY requirements.txt manage.py /app/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1
