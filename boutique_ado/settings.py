"""
Django settings for boutique_ado project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True ONLY if there is 'development' in the environment
DEBUG = 'DEVELOPMENT' in os.environ

# below I add local host to allow gitpod to work simultaneously with the deployed app
ALLOWED_HOSTS = ['gaberoids-boutiqueado.herokuapp.com', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # call URLS when connecting via social media
    # account. good to track users activity in the website for marketing
    # statistics purposes
    'allauth',
    'allauth.account',  # login and out, user registration password resets
    'allauth.socialaccount',  # login into social media
    'home',
    'products',
    'bag',
    'checkout',
    'profiles',

    # others
    'crispy_forms',
    'storages'
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

ROOT_URLCONF = 'boutique_ado.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # allow to html request access data from HTML user input or render data ex: request.method()
                'django.contrib.auth.context_processors.auth',  # required by allauth
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # if a file does not have media
                'bag.contexts.bag_contents',
            ],
            # list of all tags we want available from bootstrap4 above
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]

# from django-allauth website https://django-allauth.readthedocs.io/en/latest/installation.html
AUTHENTICATION_BACKENDS = [

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 2

# this is for cofirmation emails when a new account is created
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Code extracted from a completed project
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # this will allow email or username as username
# the following three are the basic functionality for emails when to come to creating an account
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'boutique_ado.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# below, is for when the code is not deployed . remove this default configuration when hosting static and images on the AWS host
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Database connection with AWS host
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        # below line is referring to the env variables on heroku
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
# above the link postfres come from heroku > config variables

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# the below is for toast. this is required only for people using gitpod
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# what are alll of those variable loking things? global variables?
STATIC_URL = '/static/'

# below will tell django where static files are located
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# connection to AWS
# keep the key secret because someone can still it and the creditcard in amazon could be charged
if 'USE_AWS' in os.environ:
    # Bucket Config
    AWS_STORAGE_BUCKET_NAME = 'ckz8780-boutique-ado'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Static and media files. this  goes with the code on custom_storage.py
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'


FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
# Stripe .
STRIPE_CURRENCY = 'usd'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')  # getenv=get from enVIRONMENT GITPOD
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FROM_EMAIL = 'boutiqueado@example.com'
