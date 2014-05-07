import git

branch = git.Repo().head.ref.name
deployhost = 'app-aap-tst@localhost'
sitename = 'tst-%s.templateproject.nl' % branch
projectdir = "releases/" + branch
tag = None
