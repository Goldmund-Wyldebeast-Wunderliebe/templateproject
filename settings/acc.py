from .base import *

DATABASES = { 'default': read_pgpass('app-mysite-acc'), }

from .imprint import SITE_IMPRINT_ACC as SITE_IMPRINT
