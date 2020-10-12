"""
Django settings for binary_broker project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from django.urls import reverse_lazy
from pathlib import Path
import datetime
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'secret_key.txt')) as file:
    SECRET_KEY = file.read()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    'django_extensions',
    'django_celery_results',
    'django_celery_beat',
    'channels',
    'channels_redis',
    'django_countries',
    'social_django',
    'bootstrap4',
    'crispy_forms',
    'simple_history',
    'binary_broker.applications.accounts.apps.AccountsConfig',
    'binary_broker.applications.main.apps.MainConfig',
    'binary_broker.applications.trading.apps.TradingConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'binary_broker.applications.main.middlewares.settings_middleware',
    'binary_broker.applications.trading.middlewares.trading_middleware',    
]

ROOT_URLCONF = 'binary_broker.urls'

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
                'django.template.context_processors.i18n',
                'binary_broker.applications.accounts.context_processors.auth_context_processor',
                'binary_broker.applications.trading.context_processors.trading_context_processor',
                'binary_broker.applications.main.context_processors.global_settings_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'binary_broker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Authentication

LOGIN_URL = reverse_lazy('login')
AUTH_USER_MODEL = 'accounts.CustomUser'
with open(os.path.join(BASE_DIR, 'secrets', 'api_secrets.json')) as file:
    API_SECRETS = json.load(file)
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)
SOCIAL_AUTH_URL_NAMESPACE = 'social'
with open('secrets/api_secrets.json') as file:
    api_secrets = json.load(file)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = api_secrets['google']['key']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = api_secrets['google']['secret']
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_KEY = api_secrets['facebook']['key']
SOCIAL_AUTH_FACEBOOK_SECRET = api_secrets['facebook']['secret']
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = api_secrets['github']['key']
SOCIAL_AUTH_GITHUB_SECRET = api_secrets['github']['secret']
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en-us',   'English'),
    ('fr',      'French'),
    ('de',      'German'),
    ('es',      'Spanish'),
    ('ru',      'Russian'),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR), 'static_assets'
]

# Styles, forms, etc
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
}

# Redis

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
BROKER_VHOST = '0'
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

# Channels

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

ASGI_APPLICATION = "binary_broker.channel_routing.application"

# CELERY

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'redis'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Custom

GLOBAL_UPDATE_PERIOD = datetime.timedelta(seconds=5)
