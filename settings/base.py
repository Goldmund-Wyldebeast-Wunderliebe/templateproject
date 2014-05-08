from .core import *

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': None,
        'USER': None,
        'PASSWORD': None,
        'HOST': None,
    }
}

def read_pgpass(dbname):
    import os
    pgpass = os.path.join(os.environ['HOME'], '.pgpass')
    for line in open(pgpass).read().split():
        words = line.strip().split(':')
        if words[2]==dbname:
            DATABASES['default']['NAME'] = words[2]
            DATABASES['default']['USER'] = words[3]
            DATABASES['default']['PASSWORD'] = words[4]
            DATABASES['default']['HOST'] = words[0]


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
