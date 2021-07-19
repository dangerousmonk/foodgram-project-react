# syntax=docker/dockerfile:1
FROM python:3.9.5
WORKDIR /code
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY . .
CMD gunicorn settings.wsgi:application --bind 0.0.0.0:8000
