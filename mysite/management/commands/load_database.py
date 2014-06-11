from subprocess import call
from django.conf import settings
from django.core.management.base import BaseCommand


LOAD_COMMANDS = [
    "dropdb --user=%(USER)s --host=%(HOST)s %(NAME)s",
    "createdb --user=%(USER)s --host=%(HOST)s %(NAME)s",
    "pg_restore --user=%(USER)s --host=%(HOST)s --dbname=%(NAME)s %(dumpfile)s",
    ]


LOAD_COMMANDS = [
    """
    dropdb 
        --user=%(USER)s \
        --host=%(HOST)s \
        %(NAME)s
    """,
    """
    createdb 
        --user=%(USER)s \
        --host=%(HOST)s \
        %(NAME)s
    """,
    """
    pg_restore \
            --user=%(USER)s \
            --host=%(HOST)s \
            --dbname=%(NAME)s \
            %(dumpfile)s
    """,
    ]


class Command(BaseCommand):
    def handle(self, dumpfile, **kwargs):
        env = dict(dumpfile=dumpfile)
        env.update(settings.DATABASES['default'])
        env.update(kwargs)
        for command in LOAD_COMMANDS:
            argv = [a % env for a in command.split()]
            print argv
            call(argv)
