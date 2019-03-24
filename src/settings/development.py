from .base import *  # noqa

DEBUG = True

INSTALLED_APPS += ['debug_toolbar', ]  # noqa

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]  # noqa

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
