"""
Django settings for anon_cms project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import settings_user as config
import ldap
from django_auth_ldap.config import LDAPSearch

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^xl_*lzc=qbp!9vnrrzl(6nulb%ft3n(2qbrn4+ik9gv84d(2s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMIN_USERNAMES = config.ADMIN_USERNAMES

# cache location Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Authentication Backends
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# LDAP Server URI
# http://pythonhosted.org/django-auth-ldap/authentication.html#server-config
AUTH_LDAP_SERVER_URI = "ldap://ldap.iitb.ac.in"

AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("dc=iitb,dc=ac,dc=in",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName", 
    "last_name": "sn",
    "email": 'mail',
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'stronghold',
    'account',
    'complaint',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'stronghold.middleware.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'anon_cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'anon_cms/templates/'),
            os.path.join(BASE_DIR, 'account/templates/'),
            os.path.join(BASE_DIR, 'complaint/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.static',
                'anon_cms.context.admin_usernames',
            ],
        },
    },
]

WSGI_APPLICATION = 'anon_cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# if running on test-server then sqlite can be used
# Prefer to run on postgresql 
if config.IS_TEST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'iitbcn.db',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': config.DB_ENGINE,
            'NAME': config.DB_NAME,
            'USER': config.DB_USER,
            'PASSWORD': config.DB_PASSWORD,
            'HOST': config.DB_HOST,
            'PORT': config.DB_PORT,
        }
    }

ADMINS = (
    ('Dheerendra Rathor', 'dheeru.rathor14@gmail.com'),
    )

MANAGERS = ADMINS


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'anon_cms/staticfiles/')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'anon_cms/media/')

MEDIA_URL = '/media/'

LOGIN_URL = 'account:login'

LOGIN_REDIRECT_URL = 'home:index'


STATICFILES_DIRS = (
    # Add all static files here. use os.path.join(BASE_DIR, 'your/staticfile/path')
    os.path.join(BASE_DIR, 'anon_cms/static/'),
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


# Stronghold Configuration
STRONGHOLD_PUBLIC_URLS = (
    r'^/superuser.*?$',
)
