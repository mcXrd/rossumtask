FROM python:latest

COPY requirements.txt /
RUN pip install gunicorn
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["./gunicorn.sh"]