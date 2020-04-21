FROM python:3.8-alpine

COPY requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt --no-cache-dir

COPY src .

CMD [ "gunicorn", "-w", "4", "-b", ":8080", "app:app" ]