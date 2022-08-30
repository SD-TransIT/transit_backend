"""
Django settings for transit project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
DEFAULT_SECRET_KEY = 'django-insecure-omy3k4lyrq7w8ij3uw&py!%hf@c4@4kub+mi9r-(dnn=(7=dl$'
SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!

env_hosts = os.getenv('ALLOWED_HOSTS', '').split(',')
ALLOWED_HOSTS = [host for host in env_hosts if host != '']

# Timezone info
USE_TZ = True
TIME_ZONE = os.getenv('TIMZEONE', 'UTC')

# File storages
MEDIA_URL = 'files/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT', 'files')
STATIC_ROOT = '/statics/'

f_storage = os.getenv('FILE_STORAGE', '')
if f_storage.upper() == 'AWS':
    DEFAULT_FILE_STORAGE = 'transit.custom_storage.AWSMediaStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'storages',
    'transit',
]

SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

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

ROOT_URLCONF = 'transit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'transit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'TransIT'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

LOCALE_PATHS = [
    '../locale'
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': not DEBUG,  # Swagger doesn't need authenticated user_helper in debug mode
    # Outside debug - only admin has access to swagger definition
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'base_header'
        }
    }
}

if "CORS_ORIGIN_WHITELIST" in os.environ:
    cors_hosts = os.getenv('CORS_ORIGIN_WHITELIST', '').split(',')
    CORS_ORIGIN_WHITELIST = [host for host in cors_hosts if host != '']
else:
    CORS_ALLOW_ALL_ORIGINS = True
