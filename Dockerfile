FROM python:3-alpine

EXPOSE 80
ENV FLASK_APP=run:app FLASK_ENV=docker
WORKDIR /app
COPY Pipfile.lock Pipfile /app/

RUN set -ex \
	&& apk add --no-cache --virtual .build-deps \
		gcc \
		make \
		libc-dev \
		musl-dev \
		libffi-dev \
	&& PIP_NO_CACHE_DIR=false \
	&& pip install pipenv \
	&& pipenv install --system \
	&& apk del .build-deps

COPY . /app/

CMD ["/app/entrypoint.sh"]

