"""
Django settings for system project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4@_)h@3r4y@jsx)b5(vbr@a^1@)48^+^ly(j)9ff5u(28y43e@'

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
    #
    'ws4redis',
    #
    'ddgcorp',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'system.urls'

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
                #
                'ws4redis.context_processors.default',
            ],
        },
    },
]

WSGI_APPLICATION = 'system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'base.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Update database configuration with $DATABASE_URL.

import dj_database_url

os.environ['DATABASE_URL'] = os.environ['CLEARDB_DATABASE_URL']
db_from_env = dj_database_url.config(conn_max_age=500)
if 'OPTIONS' in db_from_env and 'reconnect' in db_from_env['OPTIONS']:
    del db_from_env['OPTIONS']['reconnect']
DATABASES['default'].update(db_from_env)


# Honor the 'X-Forwarded-Proto' header for request.is_secure()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Allow all host headers

ALLOWED_HOSTS = ['*']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'ddgcorp', 'static')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'ddgcorp', 'static'),
#)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# WebSocket

WEBSOCKET_URL = '/ws/'

import dj_redis_url

try:
    REDIS_URL = os.environ['REDIS_URL']
    CAPITAL_WS4REDIS_CONNECTION = dj_redis_url.parse(REDIS_URL)
    WS4REDIS_CONNECTION = {
        'host': CAPITAL_WS4REDIS_CONNECTION['HOST'],
        'port': CAPITAL_WS4REDIS_CONNECTION['PORT'],
        'db': CAPITAL_WS4REDIS_CONNECTION['DB'],
        'password': CAPITAL_WS4REDIS_CONNECTION['PASSWORD'],
    }
    SESSION_REDIS_URL=REDIS_URL
except:
    print "REDIS_URL was not found in env"

WS4REDIS_EXPIRE = 7200

WS4REDIS_HEARTBEAT = '--heartbeat--'

WSGI_APPLICATION = 'ws4redis.django_runserver.application'
