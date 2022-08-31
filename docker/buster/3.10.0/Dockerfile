FROM python:3.10.0-buster

ARG POETRY_VERSION=1.2.0

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME=/usr/local/bin \
    VENV_PATH=/venv

RUN addgroup --gid 10001 nonroot && \
    adduser --uid 10000 --system --home /home/nonroot nonroot && \
    usermod -g nonroot nonroot

RUN apt-get update && \
    apt-get install tini --no-install-recommends -y

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv $VENV_PATH
