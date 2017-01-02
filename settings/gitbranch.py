import git
import os


def get_repo():
    d = os.path.realpath('.')
    while d != '/':
        try:
            return git.Repo(d)
        except git.InvalidGitRepositoryError:
            d = os.path.dirname(d)

repo = get_repo()
head = repo.head
if head.is_detached:
    CURRENT_BRANCH = head.object.hexsha
else:
    CURRENT_BRANCH = format(repo.active_branch)

GIT_URL = repo.remote().url

