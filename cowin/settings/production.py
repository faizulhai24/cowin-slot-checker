from .common import *
import os

DEBUG = False
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = (
    'https://www.findmyvaccine.in/',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '{0}'.format(os.getenv('POSTGRES_DB')),
        'USER': '{0}'.format(os.getenv('POSTGRES_USER')),
        'PASSWORD': '{0}'.format(os.getenv('POSTGRES_PASSWORD')),
        'HOST': '{0}'.format(os.getenv('POSTGRES_HOST')),
        'PORT': '5432',
    }
}

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)


# There is also an env variable "ENVIRONMENT" which should be set to "production"

SECRET_KEY = os.getenv("SECRET_KEY")
