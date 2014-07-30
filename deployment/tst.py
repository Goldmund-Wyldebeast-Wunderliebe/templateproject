import os
import git
from datetime import datetime

from .config import deploy_config


head = git.Repo().head
if head.is_detached:
    deploy_config.branch = head.object.hexsha
else:
    deploy_config.branch = head.ref.name

deploy_config.deployhost = 'app-mysite-tst@localhost'
deploy_config.homedir = '/opt/APPS/mysite/tst'
deploy_config.sitename = 'tst-%s.templateproject.nl' % deploy_config.branch
deploy_config.serveradmin = 'webmaster@templateproject.nl'
deploy_config.webserver = 'nginx'
deploy_config.gunicorn_workers = 1
deploy_config.projectdir = os.path.join("releases", deploy_config.branch)

