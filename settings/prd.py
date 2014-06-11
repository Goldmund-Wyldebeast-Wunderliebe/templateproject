from .base import *

DATABASES = { 'default': read_pgpass('app-mysite-prd'), }

from .imprint import SITE_IMPRINT_PRD as SITE_IMPRINT
