import git

branch = git.Repo().head.ref.name
deployhost = 'app-mysite-tst@localhost'
homedir = '/opt/APPS/mysite/tst'
sitename = 'tst-%s.templateproject.nl' % branch
serveradmin = 'webmaster@templateproject.nl'
webserver = 'nginx'
gunicorn_port = 8801
gunicorn_workers = 1
projectdir = "releases/" + branch
tag = None
