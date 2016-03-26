import os
from fabric.api import task


@task
def pick_settings(label, layer):
    with open('settings/label.py', 'wb') as fh:
        fh.write("LAYER = '%s'\nLABEL = '%s'\n" % (layer, label))
    with open('settings/__init__.py', 'wb') as fh:
        fh.write('from .%s import *\n' % layer)
    for vardir in ('log', 'run'):
        path = os.path.join('var', vardir)
        if not os.path.isdir(path):
            os.makedirs(path, mode=0700)

