import os
import sys
import git
import tempfile

from fabric.api import env, run, put, task
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.importlib import import_module

from deployment.config import deploy_config


env.forward_agent = True
env.always_use_pty = False
env.linewise = True
env.shell = '/bin/dash -e -c'


@task
def pick_settings(layer):
    file = 'settings/__init__.py'
    with open(file, 'wb') as fh:
        fh.write('from .%s import *\n' % layer)
    for vardir in ('log', 'run'):
        os.makedirs(os.path.join('var', vardir), mode=0700)

# shorthand for fab pick_settings:layer=dev
@task
def dev():
    pick_settings('dev')


def setup(layer='tst', **kwargs):
    env.layer = layer
    sys.path.append(os.getcwd())
    for k, v in kwargs.items():
        setattr(deploy_config, k, v)
    deployment_module = 'deployment.{0}'.format(env.layer)
    import_module(deployment_module)
    env.host_string = deploy_config.deployhost
    for element in [
            'branch', 'tag', 'sitename',
            'homedir', 'projectdir',
            'gunicorn_port', 'gunicorn_workers',
            'webserver', 'serveradmin',
            ]:
        setattr(env, element, getattr(deploy_config, element, None))
    env.projectdir = os.path.join(env.homedir, env.projectdir)
    env.source = git.Repo().remote().url


@task
def shutdown(unlink=False, remove=False, **kwargs):
    setup(**kwargs)

    sites_enabled_link = run("""
        readlink sites-enabled/%(sitename)s
        """ % env, warn_only=True)
    is_linked = sites_enabled_link.startswith(os.path.join(env.projectdir, ''))
    if unlink and not is_linked:
        print("Not unlinking %(sitename)s.  It's not there" % env)
        return
    elif not unlink and is_linked:
        print("Not shutting down %(sitename)s.  Unlink first" % env)
        return
    elif unlink and is_linked:
        print("unlinking %(sitename)s" % env)
        run("""
            rm -f %(homedir)s/sites-enabled/%(sitename)s
            sudo /etc/init.d/%(webserver)s reload
        """ % env)

    print("shutting down %(sitename)s" % env)
    run("""
        cd %(projectdir)s
        . bin/activate
        supervisorctl shutdown
        """ % env)

    if remove:
        print("removing down %(sitename)s" % env)
        run("""
            rm -rf %(projectdir)s
            """ % env)

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


