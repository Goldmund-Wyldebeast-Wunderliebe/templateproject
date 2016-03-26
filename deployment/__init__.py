import os
import random
from datetime import datetime
from django.conf import settings


class DeployConfig(object):
    """
    This class keeps first assignment to attributes.
    It's intended for command-line options to be passed in first
    and have related values working as expected:

    In deployment/tst.py:
    deploy_config.branch = ...
    deploy_config.projectdir = os.path.join("releases", deploy_config.branch)

    If branch is overruled on the command-line, projectdir changes
    with it.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            self.__dict__[key] = value

    def __repr__(self):
        return repr(self.__dict__)


class DeploymentLabel(DeployConfig):
    def __init__(self, **kwargs):
        self.label = 'templateproject'
        self.branches = {
                'tst': settings.CURRENT_BRANCH,
                'acc': 'acceptance',
                'prd': 'master',
                }
        self.sitenames = {
                'tst': (lambda x: 'tst-%s.templateproject.nl' % x.branch),
                'acc': 'acc.templateproject.nl',
                'prd': 'www.templateproject.nl',
                }
        # stuff below this is overruled by cmdline, stuff above isn't.
        super(DeploymentLabel, self).__init__(**kwargs)
        self.layer = 'tst'
        self.host = '127.0.0.1'
        self.timestamp = datetime.now().strftime('%Y%m%d')
        self.baseport = 8000
        self.deployhost = 'app-%s-%s@%s' % (self.label, self.layer, self.host)
        self.homedir = '/opt/APPS/%s/%s' % (self.label, self.layer)
        self.branch = self.branches[self.layer]
        sitename = self.sitenames[self.layer]
        self.sitename = sitename(self) if callable(sitename) else sitename

    def defaults(self):
        if self.layer == 'tst':
            self.gunicorn_port = random.randint(10000, 19999)
            self.gunicorn_workers = 1
            self.projectdir = os.path.join("releases", self.branch)

        elif self.layer == 'acc':
            self.gunicorn_port = self.baseport + 1
            self.gunicorn_workers = 1
            self.tag = "acc-" + self.timestamp
            self.projectdir = os.path.join("releases", self.branch)

        elif self.layer == 'prd':
            self.gunicorn_port = self.baseport
            self.gunicorn_workers = 4
            self.tag = "prd-" + self.timestamp
            self.projectdir = os.path.join("releases", self.tag)

