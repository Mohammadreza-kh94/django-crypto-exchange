#!/bin/sh

until python3 manage.py migrate
do
    echo "Waiting for postgres ready..."
    sleep 5
done

gunicorn --bind :8000 crypto_exchange_app.wsgi:application --log-level error


