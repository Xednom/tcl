"""
Django settings for tclordering project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import dj_database_url
import json
# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) original BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# EMAIL SETUP
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'monde.lacanlalay@gmail.com'
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 1025
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

ADMINS = (
    ('Richmond B. Lacanlalay', 'monde.lacanlalay@gmail.com'),
)
MANAGERS = ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'SOME+RANDOM+KEYde(%e__^s2=s&*gfra1=y@46()*1g(d0=1awmid3gy49=2!raq')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

COMPRESS_ENABLED = True


# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'ordering.apps.OrderingConfig',
    'static.apps.StaticConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd part apps
    'crispy_forms',
    'compressor',
    'fm',
    'clear_cache',
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'


MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tclordering.middleware.LoginRequiredMiddleware'
]

ROOT_URLCONF = 'tclordering.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'admin_tools.template_loaders.Loader',
                    ]),
            ],
        },
    },
]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

WSGI_APPLICATION = 'tclordering.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
         # MYSQL connection
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'tclordering$tcl',
         'USER': 'tclordering',
         'PASSWORD': 'tcladmin',
         'HOST': 'tclordering.mysql.pythonanywhere-services.com',
        'PORT': '',
        # POSTGRESQL connection for heroku
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'tcl',
        # 'USER': 'tcladmin',
        # 'PASSWORD': 'tcl',
        # 'HOST': 'localhost',
        # 'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


# ######### MEDIA CONFIGURATION
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'theme/img')
# ######### END MEDIA CONFIGURATION

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join('static'),
 )

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# SSL/TLS SETTINGS FOR DJANGO
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 1000000
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

LOGIN_REDIRECT_URL = '/ordering/'

LOGIN_URL = '/ordering/login/'

LOGIN_EXEMPT_URLS = (
    r'^admin/',
    r'^ordering/logout/$',
    r'^ordering/register/$',
    r'^ordering/reset-password/$',
    r'^ordering/reset-password/done/$',
    r'^ordering/reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^ordering/reset-password/complete/$'
)