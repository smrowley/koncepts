FROM python:3.8-alpine
#FROM arm32v7/python

RUN pip install flask guinicorn

COPY src .

CMD [ "gunicorn", "app.py" ]