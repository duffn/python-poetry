FROM python:3.7-stretch

ARG POETRY_VERSION=1.1.4
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

RUN wget --no-check-certificate --no-cookies --quiet https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-amd64 \
    && wget --no-check-certificate --no-cookies --quiet https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-amd64.sha256sum \
    && echo "$(cat tini-amd64.sha256sum)" | sha256sum -c \
    && chmod +x tini-amd64 \
    && mv tini-amd64 /usr/local/bin/tini

RUN addgroup --gid 10001 nonroot && \
    adduser --uid 10000 --system --home /home/nonroot nonroot && \
    usermod -g nonroot nonroot

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv $VENV_PATH
