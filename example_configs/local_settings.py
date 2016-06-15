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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/apps/chess-server/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/apps/chess-server/media'

#celery
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout':60}
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
