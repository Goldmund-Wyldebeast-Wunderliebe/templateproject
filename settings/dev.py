from .base import *

DEBUG = True

SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False


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

