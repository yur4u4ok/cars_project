FROM python:3.11-alpine

MAINTAINER Some Dev

ENV PYTHONBUFFERED=1

RUN apk add --no-cache gcc musl-dev mariadb-dev

#For Pillow
RUN apk add --no-cache jpeg-dev zlib-dev libjpeg

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* /tmp

RUN cd /tmp\
    && pipenv lock\
    && pipenv requirements > requirements.txt\
    && pip install -r requirements.txt

#CMD	["gunicorn", "-w", "4", "configs:wsgi", "--bind", "0.0.0.0:8000"]