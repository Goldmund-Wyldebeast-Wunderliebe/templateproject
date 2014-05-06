#!/bin/sh -ex

mkdir -p var/log var/run
virtualenv .
. bin/activate
pip install -r requirements.txt
fab dev
python manage.py syncdb --noinput --all
python manage.py migrate --fake
python manage.py collectstatic --noinput --link
python manage.py runserver 0.0.0.0:8000
