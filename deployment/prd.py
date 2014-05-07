from datetime import datetime

branch = 'master'
deployhost = 'app-aap-prd@localhost'
sitename = 'www.templateproject.nl'
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
projectdir = "releases/" + timestamp
tag = "prd-" + timestamp
