import django_on_heroku
from decouple import config

from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Disable for production
CORS_ORIGIN_ALLOW_ALL = False

ALLOWED_HOSTS = [
    'social-limn.herokuapp.com'
]


