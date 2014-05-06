import os
import sys

from fabric.api import env, run
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.importlib import import_module


def pick_settings(layer):
    settings.configure(TEMPLATE_DIRS=('.'))
    files = ['settings/__init__.py', ]
    for f in files:
        fh = open(f, 'wb')
        fh.write(render_to_string('{0}.dev'.format(f), {
            'layer': layer,
        }))
        fh.close()

# shorthand for fab pick_settings:layer=dev
def dev():
    pick_settings('dev')


def deploy(layer, branch=None):
    print 'deploying to {0}'.format(layer)
    env.layer = layer

    sys.path.append(os.getcwd())
    deployment_module = 'deployment.{0}'.format(env.layer)
    deployment_config = import_module(deployment_module)
    env.branch = branch or deployment_config.branch
    env.host_string = deployment_config.deployhost
    env.sitename = deployment_config.sitename

    run("""
        cd project
        git checkout %(branch)s
        git pull
        virtualenv .
        . bin/activate
        pip install -r requirements.txt
        fab pick_settings:layer=%(layer)s

        python manage.py collectstatic --noinput
        if [ ! -d var/log ]
        then # assume first run
            mkdir -p var/log var/run
            python manage.py syncdb --noinput --all
            python manage.py migrate --fake
            supervisord
        else
            python manage.py syncdb --noinput
            python manage.py migrate
            supervisorctl reload
        fi
        """ % env)

