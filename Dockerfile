FROM python:3

ENV PYTHONUNBUFFERED 1
ENV POETRY_DJANGO_SETTINGS_MODULE settings.local
ENV DJANGO_SETTINGS_MODULE settings.local

WORKDIR /usr/src/app

COPY . /usr/src/app/

RUN pip3 install poetry

RUN poetry install
