from django.conf import settings
import django

import os
import sys
import git
import tempfile

from fabric.api import task, env, prefix, cd, run, put
from fabric.contrib.files import exists
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.importlib import import_module


def setup(**kwargs):
    #sys.path.append(os.getcwd())
    django.setup()
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

    if exists('%(projectdir)s' % env):
        with cd('%(projectdir)s' % env):
            run('git fetch')
            run('git checkout %(branch)s' % env)
            run('git pull')
    else:
        run('git clone --branch=%(branch)s %(source)s %(projectdir)s' % env)

    #if env.layer == 'tst':
    #    run("""
    #        %(projectdir)s/scripts/dbclone.sh check %(database_name)s || (
    #            %(projectdir)s/scripts/dbclone.sh make %(database_name)s
    #        )
    #    """ % env)

    with cd('%(projectdir)s' % env):
        run("""
            hash=`md5sum requirements.txt | cut -d' ' -f1`
            venvdir=$HOME/virtualenvs/$hash
            if [ ! -d $venvdir ]
            then
                mkdir -p $venvdir
                virtualenv $venvdir
                . $venvdir/bin/activate
                pip install -r requirements.txt
            fi
            rm -f venv
            ln -s $venvdir venv
            """ % env)

    if env.tag:
        with cd('%(projectdir)s' % env):
            run('git tag -f %(tag)s' % env)
            run('git push --tags -f' % env)

    with cd('%(projectdir)s' % env):
        with prefix('. venv/bin/activate'):
            run('fab pick_settings:%(label)s,%(layer)s' % env)
            run('python manage.py collectstatic --noinput')
            #run('python manage.py compilemessages')

    make_conffile('deployment/gunicorn.conf', 'etc/')
    make_conffile('deployment/%(webserver)s.conf' % env, 'etc/')
    make_conffile('deployment/supervisord.conf', 'etc/')

    if env.layer != 'prd':
        switch(**kwargs)


@task
def switch(**kwargs):
    setup(**kwargs)
    print("switching %(layer)s to %(projectdir)s" % env)
    # follow current symlink, stop old one
    if env.layer == 'prd':
        with cd('current'):
            with prefix('. venv/bin/activate'):
                run('supervisorctl shutdown')

    # (re)start new one
    with cd('%(projectdir)s' % env):
        with prefix('. venv/bin/activate'):
            run('python manage.py migrate --noinput')
            if exists('%(projectdir)s/var/run/supervisord.sock' % env):
                run('supervisorctl reload')
            else:
                run('supervisord')
            run('rm -f var/stopped')

    # link current to new
    if env.layer == 'prd':
        run('rm -f current ; ln -s %(projectdir)s current' % env)

    # reload apache
    run('ln -fs %(projectdir)s/etc/%(webserver)s.conf %(homedir)s/sites-enabled/%(sitename)s' % env)
    run('sudo /etc/init.d/%(webserver)s reload' % env)



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


