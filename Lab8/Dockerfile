FROM python:3.12-alpine

WORKDIR /usr/src/app
COPY . .

RUN pip install django gunicorn whitenoise psycopg2-binary gevent

EXPOSE 80
CMD ["gunicorn", "-c", "gunicorn.py.ini", "djangoProject.wsgi"]