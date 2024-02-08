FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем зависимости для Postgre
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .