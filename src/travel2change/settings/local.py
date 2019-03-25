from .base import *  # noqa
from .base import env

# GENERAL
DEBUG = env.bool('DEBUG', True)
SECRET_KEY = env('SECRET_KEY', default='275r(#c+_uh4k&nbdmt*)mq)_v^689lkq&mypgpk*8e11wboo6')
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

# CACHES
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# TEMPLATES
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa F405

# EMAILS
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar', ]  # noqa F405
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']
