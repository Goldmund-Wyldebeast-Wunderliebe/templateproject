class DeployConfig(object):
    """
    This class keeps first assignment to attributes.
    It's intended for command-line options to be passed in first
    and have related values working as expected:

    In deployment/tst.py:
    deploy_config.branch = ...
    deploy_config.projectdir = os.path.join("releases", deploy_config.branch)

    If branch is overruled on the command-line, projectdir changes
    with it.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            self.__dict__[key] = value

    def __repr__(self):
        return repr(self.__dict__)


deploy_config = DeployConfig()
