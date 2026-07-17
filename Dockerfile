"""
swarmish: fast, lightweight Python service image.

Build:
  docker build -t msb-v2-aura:latest .

Run:
  docker compose up --build
"""

from python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY msb_v2 ./msb_v2
COPY tests ./tests
COPY evals ./evals
COPY proposals ./proposals
COPY clients ./clients
COPY config.yaml ./config.yaml

RUN pip install -e /app \
    && if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

EXPOSE 8765

CMD ["python", "-m", "msb_v2.api.main"]
