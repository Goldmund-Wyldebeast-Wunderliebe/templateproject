from datetime import datetime

branch = 'acceptance'
deployhost = 'app-aap-acc@localhost'
sitename = 'acc.templateproject.nl'
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
projectdir = "releases/" + timestamp
tag = "acc-" + timestamp
