from config.settings.base import *  # noqa
from config.settings.base import env

# GENERAL
DEBUG = env.bool('DEBUG', True)
SECRET_KEY = env('SECRET_KEY', default='ysevxx@=t#8v4=&!&yqf*iv^=&$%wxapyh1shdm7skx8k4d!bc')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*'])

# CACHES
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# TEMPLATES
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa F405

# EMAILS
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-debug-toolbar
INSTALLED_APPS += ('debug_toolbar', )  # noqa F405
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

# django-extensions
INSTALLED_APPS += ('django_extensions', )

THUMBNAIL_DEBUG = True
