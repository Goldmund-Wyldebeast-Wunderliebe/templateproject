from datetime import datetime

branch = 'acceptance'
deployhost = 'app-mysite-acc@localhost'
homedir = "/opt/APPS/mysite/acc"
sitename = 'acc.templateproject.nl'
serveradmin = 'webmaster@templateproject.nl'
webserver = 'nginx'
#gunicorn_port = 8802
gunicorn_workers = 1
timestamp = datetime.now().strftime('%Y%m%d')
projectdir = "releases/" + timestamp
tag = "acc-" + timestamp
