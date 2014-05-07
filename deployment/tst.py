import git

branch = git.Repo().head.ref.name
deployhost = 'app-mysite-tst@localhost'
homedir = '/opt/APPS/mysite/tst'
sitename = 'tst-%s.templateproject.nl' % branch
projectdir = "releases/" + branch
tag = None
