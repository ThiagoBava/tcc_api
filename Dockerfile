FROM python:3.8-slim-buster

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get -y install gcc
RUN apt-get -y install libpq-dev
RUN python -m pip install --upgrade pip
COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .