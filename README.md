# python-poetry

## Unmaintained

This repository is unmaintained and will not be updated further.

## What is this?

A series of [Python Docker images](https://hub.docker.com/r/duffn/python-poetry) that use [`poetry`](https://python-poetry.org/) for dependency management. Because this is what I tend to do, these images also:

- Install [`tini`](https://github.com/krallin/tini) for simple `init`.
- Use a [non-root user and a UID above 9999](https://github.com/hexops/dockerfile#run-as-a-non-root-user).

## Usage

### Simple

```dockerfile
FROM duffn/python-poetry:3.9-slim

COPY pyproject.toml poetry.lock ./
# Poetry is installed with `pip`, so active our virtual environmentn and install projects dependecies there, so they don't conflict with poetry's dependencies.
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root

WORKDIR /app
COPY . .

# Our user has an ID of 10000 and the group an ID of 10001.
RUN chown 10000:10001 -R /app

# Our non-root username.
USER nonroot

# Use `tini` to start our container.
ENTRYPOINT ["tini", "--"]
CMD ["./my-start-command.sh"]
```

### Multi-stage Build

```dockerfile
FROM duffn/python-poetry:3.9-slim as base

COPY ./poetry.lock ./pyproject.toml ./
# Only install the production dependencies in our base multi-stage build.
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root --no-dev

# Development image
FROM base as development

# Install the development dependencies as well in our development target.
RUN . $VENV_PATH/bin/activate && $POETRY_HOME/poetry install --no-root

WORKDIR /app
COPY . .

RUN chown 10000:10001 -R /app

USER nonroot

ENTRYPOINT ["tini", "--"]
CMD ["./my-start-command.sh"]

# Production image
# Build only a single target with the --target production flag.
# `docker build --target production -t my-image:latest .`
FROM base as production

# No need to install dependenices here as we have the production dependencies in our base image.
WORKDIR /app
COPY . .

RUN chown 10000:10001 -R /app

USER nonroot

ENTRYPOINT ["tini", "--"]
CMD ["./my-start-command.sh"]
```

`my-start-command.sh` could look something like:

```bash
#!/bin/bash

set -e

. /venv/bin/activate

flask run --host=0.0.0.0
```

## Tags

All images use the [official Python images](https://hub.docker.com/_/python) as their base. All images are built when code is merged to the `main` branch.

- The `X.X-<name>` tags, for example `3.9-slim` use the the version of `poetry` [listed in the GitHub Action workflow in this repository](https://github.com/duffn/python-poetry/blob/main/.github/workflows/build-and-push-images.yml).
  - If you'd like, you can also pin to a specific version of `poetry` using the `X.X-<name>-X.X.X` tags, where `X.X.X` is a version of `poetry` starting with the minimum version of `1.1.4`. For example, `3.9-slim-1.1.4`.
  - _Recommended:_ Furthermore, you can pin to a specific date by using the `X.X-<name>-<date>` tags.
- You can find all available tags on [Docker Hub](https://hub.docker.com/repository/docker/duffn/python-poetry/tags?page=1&ordering=last_updated) or the [GitHub Container Registry](https://github.com/duffn/python-poetry/pkgs/container/python-poetry/versions).

## Generation

You can find the templates that all of the Dockerfiles are generated from in the `templates` directory.

## License

[MIT](https://opensource.org/licenses/MIT)
