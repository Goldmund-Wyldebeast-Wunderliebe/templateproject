Template Project
================

---
Installation
---

First, create a postgres database called `mysite_dev` and put it's
credentials in $HOME/.pgpass, or edit settings/dev.py.
After that, the following series of commands will get you started::

    git clone git@github.com:Goldmund-Wyldebeast-Wunderliebe/templateproject.git
    cd templateproject
    virtualenv .
    . bin/activate
    pip install -r requirements.txt
    fab dev
    python manage.py syncdb --noinput
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

---
Deployment
---

Deploy to test::

    fab deploy

Deploy to acceptance or production::

    fab deploy::layer=acc
    fab deploy::layer=prd


