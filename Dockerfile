# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat && apt-get install -y procps

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i "s/\r$//g" /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
#ENV PATH="/usr/src/app:$PATH"

# copy entrypoint for celery
COPY ./entrypoint.celery.sh .
RUN sed -i "s/\r$//g" /usr/src/app/entrypoint.celery.sh
RUN chmod +x /usr/src/app/entrypoint.celery.sh

# copy project
COPY . .

WORKDIR /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]