FROM python:3.8-alpine

ARG VCS_REF

LABEL org.label-schema.vcs-ref=$VCS_REF \
    org.label-schema.vcs-url="https://github.com/smrowley/python-reverse-debugger"

COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY src .

COPY content /usr/local/etc/content

EXPOSE 8080

CMD [ "gunicorn", "-w", "4", "-b", ":8080", "app:app" ]