FROM python:3-alpine

EXPOSE 80
WORKDIR /app
COPY Pipfile.lock Pipfile /app/

RUN set -ex \
	&& apk add --no-cache --virtual .build-deps \
		gcc \
		make \
		libc-dev \
		musl-dev \
		libffi-dev \
		postgresql-dev \
	&& apk add --no-cache postgresql-libs \
	&& PIP_NO_CACHE_DIR=false \
	&& pip install pipenv \
	&& pipenv install --system \
	&& apk del .build-deps

COPY . /app/

CMD ["/app/entrypoint.sh"]

