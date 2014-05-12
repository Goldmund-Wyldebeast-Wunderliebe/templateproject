import os
from .core import BASE_DIR

# Modified from https://gist.github.com/ndarville/3452907
SECRET_FILE = os.path.join(BASE_DIR, 'var', 'secret')
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        import random
        import string
        chars = string.ascii_letters + string.digits + string.punctuation
        SECRET_KEY = ''.join([random.SystemRandom().choice(chars)
                              for i in range(50)])
        with open(SECRET_FILE, 'wb') as fh:
            os.chmod(SECRET_FILE, 0400)
            fh.write(SECRET_KEY)
    except IOError:
        Exception('Please create a %s file with random characters \
        to generate your secret key!' % SECRET_FILE)

