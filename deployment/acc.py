import os
import git
from datetime import datetime

from .config import deploy_config


deploy_config.branch = 'acceptance'
deploy_config.deployhost = 'app-mysite-acc@localhost'
deploy_config.homedir = "/opt/APPS/mysite/acc"
deploy_config.sitename = 'acc.templateproject.nl'
deploy_config.serveradmin = 'webmaster@templateproject.nl'
deploy_config.webserver = 'nginx'
deploy_config.gunicorn_workers = 1
deploy_config.timestamp = datetime.now().strftime('%Y%m%d')
deploy_config.tag = "acc-" + deploy_config.timestamp
deploy_config.projectdir = "releases/acc-" + deploy_config.timestamp

