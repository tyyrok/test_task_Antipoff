#!/bin/sh

if [ "$PGDATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PGHOST $PGPORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd app/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
exec "$@"