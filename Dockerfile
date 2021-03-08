FROM python:3.9-alpine

ARG VCS_REF
ARG BUILD_DATE

LABEL \
    org.label-schema.name="Koncepts" \
    org.label-schema.description="Python Flask app for demononstrating k8s concepts" \
    org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/smrowley/koncepts" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.version="latest" \
    org.label-schema.schema-version="1.0"

ENV LISTEN_PORT=8080
ENV METRICS_PORT=8081
ENV prometheus_multiproc_dir=/tmp
ENV CONTENT_PATH=/usr/local/etc/content
ENV COMMIT_HASH=$VCS_REF

COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY src .

COPY content $CONTENT_PATH

EXPOSE $LISTEN_PORT

CMD [ "/bin/sh", "-c", "gunicorn -c gunicorn.config.py -w 4 -b :${LISTEN_PORT} --access-logfile - --access-logformat '%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s' app:app" ]