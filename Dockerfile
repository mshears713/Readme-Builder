# syntax=docker/dockerfile:1.6

ARG PYTHON_VERSION=3.11-slim-bullseye

FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION} AS builder
ENV PIP_NO_CACHE_DIR=1
WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
COPY project_forge/requirements.txt ./project_requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install --prefix=/install -r requirements.txt -r project_requirements.txt

FROM python:${PYTHON_VERSION} AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_MODE=streamlit \
    APP_PORT=8501

RUN apt-get update && apt-get install -y --no-install-recommends curl tini && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /install /usr/local
COPY . /app

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
RUN chmod +x /app/docker/entrypoint.sh /app/docker/healthcheck.sh

USER appuser
EXPOSE 8501 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD /bin/bash /app/docker/healthcheck.sh || exit 1

ENTRYPOINT ["/bin/bash", "/app/docker/entrypoint.sh"]
