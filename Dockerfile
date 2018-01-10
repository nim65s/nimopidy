FROM node:alpine as front

RUN mkdir -p /front/public
WORKDIR /front

COPY package.json npm-shrinkwrap.json ./
COPY src src

RUN touch public/index.html && npm install && npm run build

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

RUN mkdir /back
WORKDIR /back

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY musicapp musicapp
COPY nimopidy nimopidy
COPY manage.py .

COPY --from=front /front/build /back/build
RUN mv build/static/css/main.*.css.map nimopidy/static/css/main.css.map && \
    mv build/static/css/main.*.css     nimopidy/static/css/main.css     && \
    mv build/static/js/main.*.js.map   nimopidy/static/js/main.js.map   && \
    mv build/static/js/main.*.js       nimopidy/static/js/main.js
