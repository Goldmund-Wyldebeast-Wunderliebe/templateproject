import os
import sys
import git

from fabric.api import env, run
from django.template.loader import render_to_string
from django.utils.importlib import import_module


def pick_settings(layer):
    file = 'settings/__init__.py'
    with open(file, 'wb') as fh:
        fh.write('from .%s import *\n' % layer)

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
    env.projectdir = deployment_config.projectdir
    env.tag = deployment_config.tag
    env.source = git.Repo().remote().url
    env.forward_agent = True

    run("""
        if [ -d %(projectdir)s ]
        then
            cd %(projectdir)s
            git checkout %(branch)s
            git pull
        else
            git clone --branch=%(branch)s --single-branch \
                    %(source)s %(projectdir)s
        fi
        """ % env)

    if env.tag:
        run("""
            cd %(projectdir)s
            git tag -f %(tag)s
            git push origin %(tag)s
            """ % env)

    run("""
        cd %(projectdir)s
        virtualenv .
        . bin/activate
        pip install -r requirements.txt
        fab pick_settings:layer=%(layer)s

        mkdir -p var/log var/run
        python manage.py collectstatic --noinput
        python manage.py syncdb --noinput
        python manage.py migrate
        if [ ! -f var/run/supervisord.sock ]
        then supervisord
        else supervisorctl reload
        fi
        """ % env)

