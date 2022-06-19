# FROM python:3.8-slim-buster
FROM python:3.10


# setting work directory
WORKDIR /usr/src/app


# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV DEBUG 0

# install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .


RUN python manage.py collectstatic --noinput


RUN adduser -u 99 myuser
USER myuser


CMD gunicorn ramrobazar.wsgi:application --bind 0.0.0.0:$PORT

# lint
#RUN flake8 --ignore=E501,F401 .