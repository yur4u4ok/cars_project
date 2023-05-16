FROM python:3.11-alpine

MAINTAINER Some Dev

ENV PYTHONBUFFERED=1

RUN apk add --no-cache gcc musl-dev mariadb-dev

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* /tmp

RUN cd /tmp\
    && pipenv lock\
    && pipenv requirements > requirements.txt\
    && pip install -r requirements.txt