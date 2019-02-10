"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""


import os
from kombu import Exchange, Queue

BATCH_SIZE = 1000000
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%h(!920-v_1e6)%+@)$l9t5955a4m9v&_ipgawllvk-^_$2%=0'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'django.contrib.postgres',
    'debug_toolbar',
    'django_filters',
    'rest_framework',
    'rest_framework_filters',
    'core',
    'datasets',
    'users.apps.UsersConfig'
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1'
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'anhd',
        'HOST': 'postgres',
        'USER': 'anhd',
        'PORT': '5432'
    }
}

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        "KEY_PREFIX": "DAP"
    }
}


REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.RestFrameworkFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework_csv.renderers.CSVRenderer',
    # ),
}


WSGI_APPLICATION = 'app.wsgi.application'
CACHE_TTL = 60 * 60 * 24  # cache for 24 hours
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        "KEY_PREFIX": "DAP"
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True

##
# TODO - setup flower auth
# https://flower.readthedocs.io/en/latest/reverse-proxy.html#reverse-proxy
##

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "America/New_York"
# https://stackoverflow.com/questions/19853378/how-to-keep-multiple-independent-celery-queues
# https://stackoverflow.com/questions/23129967/django-celery-multiple-queues-on-localhost-routing-not-working
# celery queues setup
CELERY_DEFAULT_QUEUE = 'celery'
CELERY_DEFAULT_EXCHANGE_TYPE = 'celery'
CELERY_DEFAULT_ROUTING_KEY = 'celery'
CELERY_QUEUES = (
    Queue('celery', Exchange('celery'), routing_key='celery'),
    Queue('update', Exchange('updates'), routing_key='updates'),
)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

MEDIA_URL = '/data/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
MEDIA_TEMP_ROOT = os.path.join(MEDIA_ROOT, 'temp')
LOG_ROOT = os.path.join(BASE_DIR, 'logs')

FLOWER_URL = "localhost:8888"
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_BACKEND = 'rpc://'
# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',

        }
    },
    'formatters': {
        'standard': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'log_colors': {
                'DEBUG':    'purple',
                'INFO':     'cyan',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        },
        'sql': {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(log_color)s[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S",
            'log_colors': {
                'DEBUG':    'bold_green',
                'INFO':     'bold_blue',
                'WARNING':  'bold_yellow',
                'ERROR':    'bold_red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'handlers': {
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "dap-council.log"),
            'maxBytes': 1024 * 1024 * 5,  # 15MB
            'backupCount': 20,
            'formatter': 'standard',
        },
        'errorfile': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_ROOT, "dap-council.error.log"),
            'maxBytes': 1024 * 1024 * 5,  # 15MB
            'backupCount': 20,
            'formatter': 'standard',
        },
        'sql': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'app': {
            'handlers': ['console', 'logfile', 'errorfile'],
            'level': 'DEBUG',
        },
    }
}

# Use exact model names from datasets/models
ACTIVE_MODELS = [
    'Council',
    'Property',
    'Building',
    'AcrisRealLegal',
    'AcrisRealMaster',
    'AcrisRealParty',
    'CoreSubsidyRecord',
    'DOBComplaint',
    'DOBPermitFiledLegacy',
    'DOBPermitIssuedLegacy',
    'DOBPermitIssuedNow',
    'DOBPermitIssuedJoined',
    'DOBViolation',
    'ECBViolation',
    'Eviction',
    'HousingLitigation',
    'HPDBuildingRecord',
    'HPDComplaint',
    'HPDProblem',
    'HPDContact',
    'HPDRegistration',
    'HPDViolation',
    'RentStabilizationRecord',
    'SubsidyJ51',
    'Subsidy421a',
    'PublicHousingRecord',
    'TaxLien',
    'LisPenden',
    'LisPendenComment'
]
