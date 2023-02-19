"""
Django settings for social_limn project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import environ
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Disable for production
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core',
    'cloudinary',
    'cloudinary_storage',
    'location_field.apps.DefaultConfig',
    "mapbox_location_field",
    'widget_tweaks',
    'bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'social_limn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            # 'loaders': [
            # ('django.template.loaders.cached.Loader', [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            #     'path.to.custom.Loader',
            #     ]),
            # ],
        },
    },
]

# CRISPY_ALLOWED_TEMPLATE_PACKS =('bulma',)
# CRISPY_TEMPLATE_PACK = 'bulma'

WSGI_APPLICATION = 'social_limn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_USER_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


# These are commented out for development purposes only ** UNCOMMENT FOR PRODUCTION!! **
AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# White listing the localhost:3000 port
# for React
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = os.path.join(BASE_DIR,'/limn/dashboard')
LOGOUT_REDIRECT_URL = os.path.join(BASE_DIR,'/accounts/login')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SEARCH_RESULTS_PER_PAGE = 10  # The number of search results to show per page
SPOTIFY_BASE_URL = "https://api.spotify.com/v1/search?q"
SPOTIFY_LIMIT = 50

IFRAME_KEY = env('IFRAME_KEY')
SPOTIPY_CLIENT_ID = env('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = env('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = env('SPOTIPY_REDIRECT_URI')

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_ROOT_URL = env('CLOUDINARY_URL')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('API_KEY'),
    'API_SECRET': env('API_SECRET') 
}

LOCATION_FIELD = {
    'map.provider': 'mapbox',
    'map.zoom': 13,
    # Mapbox
    'provider.mapbox.access_token': env('MAP_KEY'),
    'provider.mapbox.max_zoom': 18,
    'provider.mapbox.id': 'mapbox.streets',
}

MAPBOX_KEY = env('MAP_KEY')

LOCATIONIQ_API_KEY = env('LIQ')
