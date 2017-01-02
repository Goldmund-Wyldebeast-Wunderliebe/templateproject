import os
from fabric.api import env, task
from deployment.fabric.deploy import deploy, switch
from deployment.fabric.settings import pick_settings


env.forward_agent = True
env.always_use_pty = True
env.linewise = True
env.shell = '/bin/bash -e -c'
env.use_ssh_config=True

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


# shorthand for fab pick_settings:layer=dev
@task
def dev(label='templateproject'):
    pick_settings(label, 'dev')

