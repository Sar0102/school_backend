FROM python:3.11.7-alpine3.19 as base

WORKDIR /home/user/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt
