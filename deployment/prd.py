import os
import git
from datetime import datetime

from .config import deploy_config


deploy_config.branch = 'master'
deploy_config.deployhost = 'app-mysite-prd@localhost'
deploy_config.homedir = "/opt/APPS/mysite/prd"
deploy_config.sitename = 'www.templateproject.nl'
deploy_config.serveradmin = 'webmaster@templateproject.nl'
deploy_config.webserver = 'nginx'
#deploy_config.gunicorn_port = 8803
deploy_config.gunicorn_workers = 8
deploy_config.timestamp = datetime.now().strftime('%Y%m%d')
deploy_config.projectdir = "releases/prd-" + deploy_config.timestamp
deploy_config.tag = "prd-" + deploy_config.timestamp

