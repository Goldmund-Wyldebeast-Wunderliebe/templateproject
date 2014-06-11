import os
import sys
import git

from fabric.api import env, run, put
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.importlib import import_module


env.forward_agent = True
env.always_use_pty = False
env.linewise = True
env.shell = '/bin/dash -e -c'


def pick_settings(layer):
    file = 'settings/__init__.py'
    with open(file, 'wb') as fh:
        fh.write('from .%s import *\n' % layer)

# shorthand for fab pick_settings:layer=dev
def dev():
    pick_settings('dev')


def setup(layer, branch):
    env.layer = layer
    sys.path.append(os.getcwd())
    deployment_module = 'deployment.{0}'.format(env.layer)
    deployment_config = import_module(deployment_module)
    env.branch = branch or deployment_config.branch
    env.host_string = deployment_config.deployhost
    for element in [
            'homedir', 'projectdir', 'tag', 'sitename',
            'gunicorn_port', 'gunicorn_workers',
            'webserver', 'serveradmin',
            ]:
        setattr(env, element, getattr(deployment_config, element, None))
    env.source = git.Repo().remote().url


def undeploy(layer='tst', branch=None):
    setup(layer, branch)
    print('undeploying %(sitename)s' % env)

    run("""
        cd %(projectdir)s
        . bin/activate
        supervisorctl shutdown
        cd
        rm -rf %(projectdir)s
        rm sites-enabled/%(sitename)s
        """ % env)


def deploy(layer='tst', branch=None):
    setup(layer, branch)
    print('deploying %(branch)s to %(sitename)s' % env)

    run("""
        if [ -d %(projectdir)s ]
        then
            cd %(projectdir)s
            git fetch
            git checkout %(branch)s
            git pull
        else
            git clone --branch=%(branch)s %(source)s %(projectdir)s
            cd %(projectdir)s
            virtualenv .
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
        . bin/activate
        pip install -r requirements.txt
        fab pick_settings:layer=%(layer)s
        mkdir -p var/log var/run
        python manage.py collectstatic --noinput
        """ % env)

    run("""
        cd %(projectdir)s
        . bin/activate
        python manage.py syncdb --noinput
        python manage.py migrate
        if [ ! -S var/run/supervisord.sock ]
        then supervisord
        else supervisorctl reload
        fi
        """ % env)

    deployment_templates = os.path.join(
            os.path.dirname(__file__), 'deployment', 'templates')
    settings.configure(TEMPLATE_DIRS=(deployment_templates,))

    make_conffile('gunicorn.conf', 'etc/')
    if env.webserver == 'nginx':
        make_conffile('nginx.conf', '~/sites-enabled/' + env.sitename)
        run("sudo /etc/init.d/nginx reload")
    elif env.webserver == 'apache':
        make_conffile('apache2.conf', '~/sites-enabled/' + env.sitename)
        run("sudo /etc/init.d/apache2 reload")


def make_conffile(src, tgt):
    if tgt.endswith('/'):
        tgt = os.path.join(tgt, os.path.basename(src))
    if tgt.startswith('~/'):
        tgt = os.path.join(env.homedir, tgt[2:])
    else:
        tgt = os.path.join(env.projectdir, tgt)
    tmpdir = 'tmp'
    tmpfile = os.path.join(tmpdir, src)
    d = os.path.dirname(tmpfile)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(tmpfile, 'wb') as fh:
        os.chmod(tmpfile, 0644)
        fh.write(render_to_string(src, env))
    put(tmpfile, tgt)


