import git


head = git.Repo().head
if head.is_detached:
    CURRENT_BRANCH = head.object.hexsha
else:
    CURRENT_BRANCH = format(git.Repo().active_branch)
