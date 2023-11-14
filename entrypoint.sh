#!/bin/sh

if [ "$PGDATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $PGHOST $PGPORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
cd app/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
#python manage.py collectstatic --no-input
#gunicorn django_on_aws.wsgi:application --bind :8000

exec "$@"