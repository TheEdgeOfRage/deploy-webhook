FROM python:3.8-alpine AS builder

WORKDIR /app
ENV PATH="/root/.poetry/bin:$PATH"

RUN apk add --no-cache build-base git libffi-dev curl \
	&& curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python \
	&& python -m venv .venv \
	&& poetry config virtualenvs.in-project true \
	&& .venv/bin/pip install --no-cache-dir -U pip setuptools

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root --no-interaction

COPY deploy_webhook/ ./deploy_webhook/
RUN set -x \
	&& poetry install --no-dev --no-interaction \
	&& rm -rf deploy_webhook.egg-info


FROM python:3.8-alpine

EXPOSE 80
WORKDIR /app
CMD ["sh", "/app/entrypoint.sh"]
HEALTHCHECK --interval=10s --timeout=5s CMD curl http://127.0.0.1
ENV PATH="/app/.venv/bin:$PATH" \
	FLASK_APP=run:app \
	FLASK_ENV=docker \
	PYTHONUNBUFFERED=1

RUN apk add --no-cache libc-dev binutils curl && mkdir /data

COPY run.py docker/ ./
COPY migrations/ ./migrations/
COPY --from=builder /app/ ./
