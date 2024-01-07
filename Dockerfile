# syntax=docker/dockerfile:1

## build our base image (used for all stages except prod)
FROM ubuntu:22.04 as base

# set our env vars
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python

RUN --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache/apt/archives \
    apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash


FROM base as builder

RUN --mount=type=cache,target=/var/lib/apt/lists \
    --mount=type=cache,target=/var/cache/apt/archives \
    apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential

WORKDIR /tmp
RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=requirements.lock,target=requirements.lock \
    --mount=type=bind,source=requirements-dev.lock,target=requirements-dev.lock \
    --mount=type=bind,source=README.md,target=README.md \
    rye sync --no-dev --no-lock

# final stage
FROM base as final

USER 999

WORKDIR /app

COPY --from=builder --chown=999:999 /tmp/.venv /tmp/.venv
ENV PATH="/tmp/.venv/bin:$PATH"

COPY --chown=999:999 ./src/triangle_api .

EXPOSE 8000


FROM final as develop

ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]
#["uvicorn", "--host", "0.0.0.0", "--reload", "triangle_api.asgi:application"]


FROM final as prod

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "triangle_api.asgi:application"]
