from datetime import datetime

branch = 'master'
deployhost = 'app-mysite-prd@localhost'
homedir = "/opt/APPS/mysite/prd"
sitename = 'www.templateproject.nl'
serveradmin = 'webmaster@templateproject.nl'
webserver = 'nginx'
gunicorn_port = 8803
gunicorn_workers = 8
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
projectdir = "releases/" + timestamp
tag = "prd-" + timestamp
