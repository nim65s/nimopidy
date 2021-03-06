"""
Django settings for nimopidy project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from os import environ
from os.path import abspath, dirname

PROJECT = 'nimopidy'

BASE_DIR = dirname(dirname(abspath(__file__)))
ALLOWED_HOSTS = [PROJECT, 'daphne', 'localhost', 'nimopidy', environ['NIMOPIDY_HOST']]

SECRET_KEY = environ['DJANGO_SECRET_KEY']

DEBUG = environ.get('DJANGO_DEBUG', 'false').lower() == 'true'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    PROJECT,
    'bootstrap3',
    'channels',
    'ndh',
    'musicapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = f'{PROJECT}.urls'

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
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = f'{PROJECT}.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': environ.get('POSTGRES_USER', PROJECT),
        'NAME': environ.get('POSTGRES_NAME', PROJECT),
        'HOST': environ.get('POSTGRES_HOST', PROJECT),
        'PASSWORD': environ['POSTGRES_PASSWORD']
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = environ.get('LANGAGE_CODE', 'fr-FR')

TIME_ZONE = environ.get('TIME_ZONE', 'Europe/Paris')

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = '/srv/static/'
MEDIA_ROOT = '/srv/media/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

SITE_ID = 1

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(environ.get('REDIS_HOST', PROJECT), 6379)],
        },
        'ROUTING': f'{PROJECT}.routing.channel_routing',
    },
}

MOPIDY_HOST = environ.get('MOPIDY_HOST', PROJECT)
MOPIDY_PORT = environ.get('MOPIDY_PORT', 6680)
SNAPSERVER_HOST = environ.get('SNAPSERVER_HOST', PROJECT)
SNAPSERVER_PORT = environ.get('SNAPSERVER_PORT', 1705)
