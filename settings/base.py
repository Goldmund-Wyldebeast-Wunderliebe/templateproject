from .core import *
from .secret import SECRET_KEY


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


DATABASES = {
    'default': None,  # To be filled in in the settings/{dev,tst,acc,prd}.py
}

def read_pgpass(dbname):
    import os
    try:
        pgpass = os.path.join(os.environ['HOME'], '.pgpass')
        pgpass_lines = open(pgpass).read().split()
    except IOError:
        print """
        You don't have a ~/.pgpass file so we're using a sqlite database.
        
        To switch to a PostgreSQL database, create a ~/.pgpass file
        containing it's credentials.
        See http://www.postgresql.org/docs/9.3/static/libpq-pgpass.html
        """
    else:
        for line in pgpass_lines:
            words = line.strip().split(':')
            if words[2]==dbname:
                return {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': words[2],
                    'USER': words[3],
                    'PASSWORD': words[4],
                    'HOST': words[0],
                }

        print """
        Your ~/.pgpass file doesn't have database '%s' so we're using
        a sqlite database for now.
        
        To switch to a PostgreSQL database, add a line to the ~/.pgpass file
        containing it's credentials.
        See http://www.postgresql.org/docs/9.3/static/libpq-pgpass.html
        """
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'var', 'mysite.db'),
    }


SECURE_SSL_REDIRECT=True
SECURE_FRAME_DENY=False
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_HSTS_SECONDS=3600
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'ssl')


SITE_ID = 1
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'nl'
LANGUAGES = [
    ('nl', 'Nederlands'),
    ('en', 'English'),
]

CMS_TEMPLATES = (
    ('one_column.html', 'One Column'),
    ('two_column.html', 'Two Column'),
    ('three_column.html', 'Three Column'),
    ('homepage.html', 'Home Page'),
)


INSTALLED_APPS = (
    'mysite',
    'south',
    'mptt',
    'menus',
    'sekizai',
    'djangocms_link',
    'djangocms_text_ckeditor',  # note this needs to be above the 'cms' entry
    'cms',
    #'cms.plugins.text',
    'djangocms_twitter',
    'djangocms_file',
    'djangocms_flash',
    'djangocms_googlemap',
    'djangocms_picture',
    'djangocms_teaser',
    'djangocms_video',
    'djangocms_admin_style',
    'django.contrib.messages',
    'reversion',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.cms_settings',
    'sekizai.context_processors.sekizai',
    'mysite.context_processors.site_imprint',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'var', 'log', 'mysite.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

