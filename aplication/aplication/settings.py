"""
Django settings for aplication project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import environ
import os

env=environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#print(BASE_DIR)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3%lle9y32d&@nlhqjapiwi+*9#g4o68=6zu@(z5-t+kx0w^1fy'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True

DEBUG = env.bool('DEBUG',default=False)

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS',default=['localhost']))
#ALLOWED_HOSTS = ['localhost']
## modelo usuario
AUTH_USER_MODEL="seguridad.Usuario"
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.seguridad',
    'apps.venta',
    'apps.migracion',
    'apps.configuracion',
    'colorfield',
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

ROOT_URLCONF = 'aplication.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'aplication.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str('DATA_BASE_ENGINE'),
        #'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': env.str('DATA_BASE_NAME'),
        'USER': env.str('DATA_BASE_USER'),
        'PASSWORD':env.str('DATA_BASE_PASSWORD'),
        'HOST': env.str('DATA_BASE_HOST'),
        'PORT': env.int('DATA_BASE_PORT'),
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

TIME_ZONE = 'UTC'#'America/New_York'#'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

if DEBUG:
    SENDFILE_BACKEND = 'sendfile.backends.development'
    STATICFILES_DIRS =(BASE_DIR,'static')
else:
    STATIC_ROOT=os.path.join(BASE_DIR,'static')
    SENDFILE_BACKEND = 'sendfile.backends.nginx'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL='login'
LOGIN_REDIRECT_URL='venta'
LOGOUT_REDIRECT_URL='login'


