"""
Django settings for sirius_task_manager project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+2at1d=bwx441k9v2z@b(neqazfht3y)c2n6kjt1kx&qw%(xx@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'salty-springs-72589.herokuapp.com',
]

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
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'core.apps.ApplicationConfig',
    'task_manager.apps.TastManagerConfig',
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

ROOT_URLCONF = 'sirius_task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'sirius_task_manager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if os.environ.get('DATABASE_URL') is not None:
    DATABASES = {
        'default': dj_database_url.config()
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# User uploads (Avatars, Attachments, files uploaded in other Django apps, ect.)
# https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

MEDIA_URL = '/media/'

# The absolute path to the directory where collectstatic will collect static files for deployment.
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#static-root

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#media-root

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder
# is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.
# https://docs.djangoproject.com/en/1.10/ref/settings/#staticfiles-dirs

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
]

from .drf_settings import REST_FRAMEWORK

SITE_ADDRESS = 'http://sirius.dev'
AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['rest_framework_filters.backends.DjangoFilterBackend'],
}