# Django settings for wwdb_proj project.

from pathlib import Path
import os

import django_stubs_ext

django_stubs_ext.monkeypatch()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# URL redirect user upon successful user login
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p!kqj*)xy^*j-(5yyefrh=2@ri+b9xtcqs)-4t$xyij3d76ylx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]

CSRF_TRUSTED_ORIGINS = ['http://192.168.2.5:8081','http://192.168.1.90:8081','http://localhost:8081''http://winch.local:8081',]

CSRF_COOKIE_SECURE = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wwdb',
    'accounts',
    'bootstrap4',
    'bootstrap_datepicker_plus',
    'django_filters',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

BOOTSTRAP_DATEPICKER_PLUS = {
    # Options for all input widgets
    # More options: https://getdatepicker.com/4/Options/
	#
    # Advanced: Choose where from static JS/CSS files are served.
    # defaults: https://github.com/monim67/django-bootstrap-datepicker-plus/blob/5.0.0/src/bootstrap_datepicker_plus/settings.py#L16
    # To serve from any other preferred CDN, just update the options below.
    # You can also set them to None if you already have the following resources
    # included into your template.
    #
    "datetimepicker_js_url": None,
    "datetimepicker_css_url": None,
    "momentjs_url": None,  # If you already have momentjs added into your template
    "bootstrap_icon_css_url": None,  # If you don't need bootstrap icons
    #
    # If you want to serve static files yourself without CDN (from staticfiles) and
    # you know how to serve django static files on production server (DEBUG=False)
    # Then download the js/css files to any of your static directory, update the js/css
    # urls above and set the following option
    #
     "app_static_url": "bootstrap_datepicker_plus/",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wwdb_proj.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'context_processors.cast_context',
)

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
                'context_processors.cast_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'wwdb_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'winchdb.db',
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

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'root')
STATICFILES_DIRS =[
    os.path.join(BASE_DIR / 'static'),
    ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'timestamp': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'timestamp',
            'filename': os.path.join(BASE_DIR / 'wwdb_proj/debug.log'),
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
