from .base import *

DEBUG = True
TEMPLATE_DEBUG=DEBUG

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False


DATABASES = { 'default': read_pgpass('mysite_dev'), }

LOGGING['loggers'] = {
    'django.request': {
        'handlers': ['console', 'mail_admins'],
        'level': 'DEBUG',
        'propagate': True,
        },
    'django.db.backends': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
        },
    '': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
        },
}

from .imprint import SITE_IMPRINT_DEV as SITE_IMPRINT
