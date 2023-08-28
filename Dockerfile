# syntax=docker/dockerfile:1

## build our base image (used for all stages except prod)
FROM cgr.dev/chainguard/python:latest-dev as base

# set our env vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    BUILDER_DIR="/opt/build/" \
    VENV_PATH="/opt/build/.venv" \
    APP_DIR="/app"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:${PATH}"


## This is the base builder image (contains poetry and non dev deps)
FROM base as builder-base

USER root
RUN apk add curl

# install poetry
RUN --mount=type=cache,target=/root/.cache \
    curl -sSL https://install.python-poetry.org | python3 -

# copy project requirement files here to ensure they will be cached.
WORKDIR $BUILDER_DIR
COPY poetry.lock pyproject.toml ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --without=dev


## the builder dev image
FROM builder-base as builder-dev

WORKDIR $BUILDER_DIR

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-root --with=dev

## this is our development image
# to use: https://docs.docker.com/build/building/multi-stage/#stop-at-a-specific-build-stage
FROM base as develop

ENV FASTAPI_ENV=development \
    PATH="$VENV_PATH/bin:$PATH"
WORKDIR $APP_DIR

# copy in our built poetry + venv
COPY --from=builder-base $BUILDER_DIR $BUILDER_DIR

# mount application here repo base here (-v "$(pwd):/app")
WORKDIR $APP_DIR

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--reload", "triangle_api.asgi:application"]


## This is our production image
FROM cgr.dev/chainguard/python:latest as prod


# venv is hardcoded here since this is from a different chain of stages
ENV FASTAPI_ENV=production \
    PATH="/opt/build/.venv/bin:$PATH"

COPY --from=builder-base /opt/build/.venv /opt/build/.venv

WORKDIR /app

# only copy in the applications files for prod (no tests etc..)
COPY ./src/triangle_api .

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "triangle_api.asgi:application"]
