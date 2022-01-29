FROM python:3.8.12-alpine3.15 as backend
ENV PYTHONUNBUFFERED 1
ENV DEBUG 'True'
WORKDIR /code

# Install nginx to serve static files
RUN apk --no-cache add nginx=1.20.2-r0 bash

# Install application dependencies
COPY requirements.txt .
RUN apk --no-cache add \
        jpeg \
        libffi \
        postgresql-libs \
        tzdata \
        libxslt-dev \
        && \
    apk --no-cache add \
        --virtual .requirements-build-deps \
        gcc \
        build-base \
        jpeg-dev \
        libffi-dev \
        musl-dev \
        postgresql-dev \
        zlib-dev \
        && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .requirements-build-deps

COPY . /code/

RUN  mkdir -p /run/nginx/
COPY docker/nginx-app.conf /etc/nginx/http.d/default.conf
COPY docker/gunicorn.conf.py /code/gunicorn.conf.py
COPY docker/supervisord.conf /etc/supervisord.conf

VOLUME [ "/code/media" ]
EXPOSE 8000

ENTRYPOINT [ "/code/entrypoint.sh" ]
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
