# define the global arguments
ARG PYTHON_VERSION=3.8

# base image
FROM python:${PYTHON_VERSION} as base

LABEL MAINTAINER "Mohammadreza Khoobbakht <f69.khoobbakht@gmail.com>"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

# set work directory
COPY . /src/

WORKDIR /src

# Create a media directory
RUN mkdir media

RUN pip install --upgrade pip && pip install --no-cache-dir -r /src/requirements.txt

ENTRYPOINT [ "./django-entrypoint.sh" ]
