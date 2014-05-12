Template Project
================

---
Installation
---

The following series of commands will get you started::

    git clone git@github.com:Goldmund-Wyldebeast-Wunderliebe/templateproject.git
    cd templateproject
    mkdir -p var/log var/run
    virtualenv .
    . bin/activate
    pip install -r requirements.txt
    fab dev
    python manage.py syncdb --noinput --all
    python manage.py migrate --fake
    python manage.py collectstatic --noinput --link
    python manage.py runserver

---
Deployment
---

Deploy to test::

    fab deploy

Deploy to acceptance or production::

    fab deploy::layer=acc
    fab deploy::layer=prd


