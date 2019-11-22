FROM python:3-alpine

EXPOSE 80
ENV FLASK_APP=run:app FLASK_ENV=docker
WORKDIR /app
CMD ["/app/entrypoint.sh"]

COPY Pipfile.lock Pipfile /app/

RUN set -ex \
	&& apk add --no-cache --virtual .build-deps \
		gcc \
		make \
		musl-dev \
		libffi-dev \
	&& apk add --no-cache \
		libc-dev \
		binutils \
	&& PIP_NO_CACHE_DIR=false \
	&& pip install pipenv \
	&& pipenv install --system \
	&& apk del .build-deps

COPY . /app/

