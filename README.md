# python-poetry

## What is this?

A series of Docker Python images that use `poetry` as the dependency manager. These images also:

- Install [`tini`](https://github.com/krallin/tini) for simple `init`.
- Use a [non-root user and a UID above 10000](https://github.com/hexops/dockerfile#run-as-a-non-root-user).
- Create a virtual environment in `/venv`.

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
ENTRYPOINT ["tini", "--", "./my-start-command.sh"]
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

ENTRYPOINT ["tini", "--", "./my-start-command.sh"]

# Production image
# Build only a single target with the --target production flag.
# `docker build --target production -t my-image:latest .`
FROM base as production

# No need to install dependenices here as we have the production dependencies in our base image.
WORKDIR /app
COPY . .

RUN chown 10000:10001 -R /app

USER nonroot

ENTRYPOINT ["tini", "--", "./my-start-command.sh"]
```

`my-start-command.sh` could look something like:

```bash
#!/bin/bash

set -e

. /venv/bin/activate

flask run --host=0.0.0.0
```

## License

[MIT](https://opensource.org/licenses/MIT)
