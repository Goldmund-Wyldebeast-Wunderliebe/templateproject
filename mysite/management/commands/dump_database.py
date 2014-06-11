from subprocess import call
from django.conf import settings
from django.core.management.base import BaseCommand


DUMP_COMMAND = """
    pg_dump \
            --no-owner \
            --format=custom \
            --compress=9 \
            --file=%(dumpfile)s \
            --user=%(USER)s \
            --host=%(HOST)s \
            %(NAME)s
    """


class Command(BaseCommand):
    def handle(self, dumpfile, **kwargs):
        env = dict(dumpfile=dumpfile)
        env.update(settings.DATABASES['default'])
        env.update(kwargs)
        argv = [a % env for a in DUMP_COMMAND.split()]
        call(argv)
