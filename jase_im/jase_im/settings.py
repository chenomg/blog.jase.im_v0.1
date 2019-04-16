"""
Django settings for jase_im project.

Generated by 'django-admin startproject' using Django 1.11.15.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import django
from .logger import LOGGING

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'collected_static')
DJANGO_STATIC = os.path.join(
    os.path.dirname(os.path.abspath(django.__file__)), 'contrib', 'admin',
    'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y+o(b=flohs@l67vmw06om4xxka2p6!ee8be*pz$%+y#2x16b4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '.jase.im',
    '127.0.0.1',
    'localhost',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'api',
    'homepage',
    'markdown',
    'mdeditor',
    'registration',
    'google_analytics',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    'dashboard',
    'ssl_verify',
    'django_xmlrpc',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

GOOGLE_ANALYTICS = {
    'google_analytics_id': 'UA-119028437-1',
}

REST_FRAMEWORK = {
    # Use Django's standard 'django.contrib.auth' permission,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.utils.auth.AnonymousOrTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'api.utils.permissions.HasTokenOrReadOnly',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.authentication.BasicAuthentication',],
    'IMAGE_TYPES': ['jpg', 'jpeg', 'png', 'bmp', 'icon', 'gif'],
    'DEFAULT_THROTTLE_CLASSES': [
        'api.utils.throttle.AnonRateThrottle',
        'api.utils.throttle.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'AnonymousUser': '50/m',
        'NormalUser': '100/m',
    },
    # 设置代理数量
    # 'NUM_PROXIES': 1,
    "DEFAULT_VERSIONING_CLASS":
    "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION":
    'v1',  #默认的版本
    "ALLOWED_VERSIONS": [
        'v1',
    ],  #允许的版本
    "VERSION_PARAM":
    'version',  #get方式url中参数的名字  ?version=xxxk
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser"
    ],
}

ROOT_URLCONF = 'jase_im.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMP_DIR,
        ],
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

WSGI_APPLICATION = 'jase_im.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
    STATIC_DIR,
    MEDIA_ROOT,
    DJANGO_STATIC,
]

MDEDITOR_CONFIGS = {
    'default': {
        'width':
        '100% ',  # Custom edit box width
        'heigth':
        500,  # Custom edit box height
        'toolbar': [
            "undo", "redo", "|", "bold", "del", "italic", "quote", "ucwords",
            "uppercase", "lowercase", "|", "h1", "h2", "h3", "h5", "h6", "|",
            "list-ul", "list-ol", "hr", "|", "link", "reference-link", "image",
            "code", "preformatted-text", "code-block", "table", "datetime"
            "emoji", "html-entities", "pagebreak", "goto-line", "|", "help",
            "info", "||", "preview", "watch", "fullscreen"
        ],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp",
                                 "webp"],  # image upload format type
        'image_floder':
        'uploads',  # image save the folder name
        'theme':
        'default',  # edit box theme, dark / default
        'preview_theme':
        'default',  # Preview area theme, dark / default
        'editor_theme':
        'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed':
        True,  # Whether the toolbar capitals
        'search_replace':
        True,  # Whether to open the search for replacement
        'emoji':
        True,  # whether to open the expression function
        'tex':
        True,  # whether to open the tex chart function
        'flow_chart':
        True,  # whether to open the flow chart function
        'sequence':
        True  # Whether to open the sequence diagram function
    }
}

# 开放注册
REGISTRATION_OPEN = 'True'
# 登陆有效时间
ACCOUNT_ACTIVATION = 7
# 自动登录
REGISTRATION_AUTO_LOGIN = True
# 登陆后跳转地址
LOGIN_REDIRECT_URL = '/blog/'
# 登陆地址
LOGIN_URL = '/accounts/login/'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
INTERNAL_IPS = ('127.0.0.1', )
