from django.conf import settings

import os
import sys
import git
import tempfile

from fabric.api import env, run, put, task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.importlib import import_module


def setup(**kwargs):
    sys.path.append(os.getcwd())
    module = import_module('labels.%s' % settings.LABEL)
    deploy_config = module.deploy_class(**kwargs)
    env.host_string = deploy_config.deployhost
    for element in [
            'layer', 'label',
            'branch', 'tag', 'sitename',
            'homedir', 'projectdir',
            'gunicorn_port', 'gunicorn_workers',
            'webserver', 'serveradmin',
            ]:
        setattr(env, element, getattr(deploy_config, element, None))
        print "%s = %s" % (element, getattr(deploy_config, element, None))
    env.projectdir = os.path.join(env.homedir, env.projectdir)
    env.source = git.Repo().remote().url


@task
def deploy(**kwargs):
    setup(**kwargs)
    print("deploying %(branch)s to %(sitename)s" % env)

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
    make_conffile('nginx.conf', 'etc/')
    make_conffile('apache2.conf', 'etc/')

    if env.webserver in ['nginx', 'apache2']:
        run("""
            rm -f %(homedir)s/sites-enabled/%(sitename)s
            ln -s %(projectdir)s/etc/%(webserver)s.conf \
                    %(homedir)s/sites-enabled/%(sitename)s
            sudo /etc/init.d/%(webserver)s reload
        """ % env)


def make_conffile(src, tgt):
    if tgt.endswith('/'):
        tgt = os.path.join(tgt, os.path.basename(src))
    if tgt.startswith('~/'):
        tgt = os.path.join(env.homedir, tgt[2:])
    else:
        tgt = os.path.join(env.projectdir, tgt)
    tmpdir = tempfile.mkdtemp()
    print tmpdir
    tmpfile = os.path.join(tmpdir, src)
    d = os.path.dirname(tmpfile)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(tmpfile, 'wb') as fh:
        os.chmod(tmpfile, 0644)
        fh.write(render_to_string(src, env))
    put(tmpfile, tgt)
    os.unlink(tmpfile)
    os.removedirs(tmpdir)


