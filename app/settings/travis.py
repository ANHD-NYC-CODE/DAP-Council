from app.settings.base import *
CELERY_BROKER_URL = 'redis://localhost:6379'
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'anhd',
        'HOST': 'localhost',
        'USER': 'postgres',
        'PORT': '5432'
    }
}
