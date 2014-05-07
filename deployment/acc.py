from datetime import datetime

branch = 'acceptance'
deployhost = 'app-mysite-acc@localhost'
homedir = "/opt/APPS/mysite/acc"
sitename = 'acc.templateproject.nl'
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
projectdir = "releases/" + timestamp
tag = "acc-" + timestamp
