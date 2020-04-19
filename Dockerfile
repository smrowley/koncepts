FROM python:3.8-alpine
#FROM arm32v7/python

COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

COPY src .

CMD [ "gunicorn", "-w", "4", "-b", ":8080", "app:app" ]