import os


def read_pgpass(dbname):
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
        for match in (dbname, '*'):
            for line in pgpass_lines:
                words = line.strip().split(':')
                if words[2] == match:
                    return {
                        'ENGINE': 'django.db.backends.postgresql_psycopg2',
                        'NAME': dbname,
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
        """ % dbname
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'var', 'mysite.db'),
    }

