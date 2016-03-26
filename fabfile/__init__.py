import os
from fabric.api import env, task
import django
from .deploy import deploy


env.forward_agent = True
env.always_use_pty = False
env.linewise = True
env.shell = '/bin/dash -e -c'
env.use_ssh_config=True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()


@task
def pick_settings(layer, label):
    with open('settings/label.py', 'wb') as fh:
        fh.write("LAYER = '%s'\nLABEL = '%s'\n" % (layer, label))
    with open('settings/__init__.py', 'wb') as fh:
        fh.write('from .%s import *\n' % layer)
    for vardir in ('log', 'run'):
        path = os.path.join('var', vardir)
        if not os.path.isdir(path):
            os.makedirs(path, mode=0700)


# shorthand for fab pick_settings:layer=dev
@task
def dev(label='templateproject'):
    pick_settings('dev', label)

