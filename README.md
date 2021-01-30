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

# Copy installed production dependencies from the base image and then install the development dependencies as well.
COPY --from=base $VENV_PATH $VENV_PATH
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

# Copy production dependecies from the base image. There's no need to install anything more.
COPY --from=base $VENV_PATH $VENV_PATH

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
