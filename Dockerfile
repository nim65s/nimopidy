FROM python:latest

ENV PYTHONUNBUFFERED=1 \
   NIMOPIDY_HOST=nimopidy \
   REDIS_HOST=redis \
   MOPIDY_HOST=mopidy \
   SNAPSERVER_HOST=snapserver \
   POSTGRES_HOST=postgres \
   POSTGRES_USER=postgres \
   POSTGRES_NAME=postgres \
   POSTGRES_PASSWORD=placeholder \
   DJANGO_SECRET_KEY=placeholder \
   DJANGO_DEBUG=False \
   LANGAGE_CODE=fr-FR \
   TIME_ZONE=Europe/Paris

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
