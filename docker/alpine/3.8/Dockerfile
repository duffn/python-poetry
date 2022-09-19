FROM python:3.8-alpine

ARG POETRY_VERSION=1.2.1
ARG TINI_VERSION=v0.19.0

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME=/usr/local/bin \
    VENV_PATH=/venv \
    TINI_VERSION=${TINI_VERSION}

RUN apk update \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo

RUN wget --no-check-certificate --quiet https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-amd64 \
    && wget --no-check-certificate --quiet https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-amd64.sha256sum \
    && echo "$(cat tini-amd64.sha256sum)" | sha256sum -c \
    && chmod +x tini-amd64 \
    && mv tini-amd64 /usr/local/bin/tini

RUN addgroup --gid 10001 nonroot && \
    adduser --ingroup nonroot --uid 10000 --system --home /home/nonroot nonroot

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv $VENV_PATH
