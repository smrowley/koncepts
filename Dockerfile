ARG BASE_IMAGE=python:3.8-alpine

FROM ${BASE_IMAGE}
#FROM arm32v7/python

COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY src .

CMD [ "gunicorn", "-w", "4", "-b", ":8080", "app:app" ]