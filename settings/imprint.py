import git

head = git.Repo().head
if head.is_detached:
    branch = head.object.hexsha
else:
    branch = format(git.Repo().active_branch)

SITE_IMPRINT_DEV = 'dev:' + branch
SITE_IMPRINT_TST = 'tst:' + branch
SITE_IMPRINT_ACC = 'acc'
SITE_IMPRINT_PRD = ''
