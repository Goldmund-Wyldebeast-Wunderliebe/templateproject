from .base import *

DEBUG = True
TEMPLATE_DEBUG=DEBUG

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False

read_pgpass('app-mysite-tst')

from .imprint import SITE_IMPRINT_TST as SITE_IMPRINT
