from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _
import environ

BASE_DIR = environ.Path(__file__) - 3  # /config/settings/base.py - 3 = /
DATA_DIR = BASE_DIR.path('travel2change')

env = environ.Env()
env.read_env()

gettext = lambda s: s # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en'

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
SITE_DOMAIN = env('SITE_DOMAIN', default='127.0.0.1:8000')

# Google API
GOOGLE_MAPS_API = env('GOOGLE_MAPS_API')

# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Pacific/Honolulu'

# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# http://docs.django-cms.org/en/latest/how_to/install.html#language-settings
LANGUAGES = (
    ('en', gettext('en')),
)

# APPS
# ------------------------------------------------------------------------------
# Django Core Apps
DJANGO_APPS = (
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.redirects',
)
# Django CMS Apps
DJANGO_CMS_APPS = (
    'djangocms_modules',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'meta',
    'easy_thumbnails',
    'djangocms_page_meta',
    'djangocms_column',
    'djangocms_file',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    'djangocms_icon',
    'djangocms_transfer',
    'djangocms_history',
    'djangocms_attributes_field',
)
# Django CMS Bootstrap Apps
DJANGO_CMS_BOOTSTRAP_APPS = (
    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',
)
# Third party apps
THIRD_PARTY_APPS = (
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'autoslug',
    'axes',
    'crispy_forms',
    'django_cleanup.apps.CleanupConfig',
    'django_filters',
    'django_social_share',
    'formtools',
    'sorl.thumbnail',
)
# Local (travel2change) apps
LOCAL_APPS = (
    'users',
    'activities',
    'moderations',
    'favorites',
    'reviews',
    'points',
    'travel2change',
)
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + DJANGO_CMS_APPS + DJANGO_CMS_BOOTSTRAP_APPS + THIRD_PARTY_APPS

# URLS
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'

# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {'default': env.db('DATABASE_URL'), }
DATABASES['default']['ATOMIC_REQUESTS'] = True

# MIGRATIONS
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {}

# AUTHENTICATION
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesModelBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.CustomUser'

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "/"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'

# PASSWORDS
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# EMAIL
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ALLOW_REGISTRATION = env.bool('ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {'signup': 'users.forms.SignupForm'}

# MIDDLEWARE
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR('staticfiles'))

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (str(DATA_DIR.path('static')), )

# MEDIA
# https://docs.djangoproject.com/en/2.2/topics/files/

# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(BASE_DIR('media'))

# TEMPLATES
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(DATA_DIR.path('templates')),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]
# Django Crispy Forms
# https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_CLASS_CONVERTERS = {
    'textinput': "form-control cst__radius",
    'urlinput': "form-control cst__radius",
    'numberinput': "form-control cst__radius",
    'emailinput': "form-control cst__radius",
    'dateinput': "form-control cst__radius",
    'textarea': "form-control cst__radius",
    'passwordinput': "form-control cst__radius",
    'select': "form-control cst__radius",
}

# Django Messages
# https://docs.djangoproject.com/en/2.2/ref/contrib/messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# DJANGO CMS
# http://docs.django-cms.org/en/latest/reference/configuration.html#std:setting-CM

# http://docs.django-cms.org/en/latest/reference/configuration.html#cms-languages
CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': gettext('en'),
            'redirect_on_fallback': True,
            'public': True,
            'hide_untranslated': False,
        },
    ],
    'default': {
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,
    },
}

# http://docs.django-cms.org/en/latest/introduction/02-templates_placeholders.html?highlight=CMS_TEMPLATES#templates
CMS_TEMPLATES = (
    ('home.html', 'Homepage'),
    ('default_page.html', 'Default'),
)

# http://docs.django-cms.org/en/latest/topics/permissions.html#cms-permission-mode
CMS_PERMISSION = True

# http://docs.django-cms.org/en/latest/reference/configuration.html#std:setting-CMS_PLACEHOLDER_CONF
CMS_PLACEHOLDER_CONF = {}

# https://easy-thumbnails.readthedocs.io/en/latest/ref/settings/#easy_thumbnails.conf.Settings.THUMBNAIL_PROCESSORS
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

# Django CMS Bootstrap
# https://github.com/divio/djangocms-bootstrap4
DJANGOCMS_BOOTSTRAP4_TAG_CHOICES = ['div', 'section', 'article', 'header', 'footer', 'aside']
DJANGOCMS_BOOTSTRAP4_CAROUSEL_TEMPLATES = (
    ('default', _('Default')),
)
DJANGOCMS_BOOTSTRAP4_GRID_SIZE = 12
DJANGOCMS_BOOTSTRAP4_GRID_CONTAINERS = (
    ('container', _('Container')),
    ('container-fluid', _('Fluid container')),
)
DJANGOCMS_BOOTSTRAP4_GRID_COLUMN_CHOICES = (
    ('col', _('Column')),
    ('w-100', _('Break')),
    ('', _('Empty'))
)
DJANGOCMS_BOOTSTRAP4_USE_ICONS = True
DJANGOCMS_BOOTSTRAP4_TAB_TEMPLATES = (
    ('default', _('Default')),
)
DJANGOCMS_BOOTSTRAP4_SPACER_SIZES = (
    ('0', '* 0'),
    ('1', '* .25'),
    ('2', '* .5'),
    ('3', '* 1'),
    ('4', '* 1.5'),
    ('5', '* 3'),
)
DJANGOCMS_BOOTSTRAP4_CAROUSEL_ASPECT_RATIOS = (
    (16, 9),
)
DJANGOCMS_BOOTSTRAP4_COLOR_STYLE_CHOICES = (
    ('primary', _('Primary')),
    ('secondary', _('Secondary')),
    ('success', _('Success')),
    ('danger', _('Danger')),
    ('warning', _('Warning')),
    ('info', _('Info')),
    ('light', _('Light')),
    ('dark', _('Dark')),
    ('custom', _('Custom')),
)

# Django Axes
# https://django-axes.readthedocs.io/en/latest/index.html
AXES_USERNAME_FORM_FIELD = 'login'

# Other Settings

# Maximum Photos per Activity
MAX_PHOTOS_PER_ACTIVITY = 5
