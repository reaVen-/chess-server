from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'user',
        'PASSWORD' : 'password',
        'HOST' : 'localhost',
        'PORT' : '5432',
            }
}