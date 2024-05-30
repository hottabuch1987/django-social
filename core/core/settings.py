from datetime import timedelta
from pathlib import Path

import environ
from django.contrib import messages
import os


BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()
env.read_env()




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', "http://195.133.32.53", "195.133.32.53", "localhost",]

#"http://195.133.32.53", "195.133.32.53",

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #libs
    'mathfilters',
    'crispy_forms',
    "crispy_bootstrap5",
    'django_email_verification',
    'django_google_fonts',
    "sorl.thumbnail",
    "django_celery_beat",
    "django_celery_results",
    "django_htmx",
    'django_recaptcha',
    'django_filters',

    'rest_framework',
    'djoser',
    'drf_yasg',
    "channels",

    'channels_redis',

    "social_django",
    'ckeditor',
    'ckeditor_uploader',

    #apps
    'shop.apps.ShopConfig',
    'account.apps.AccountConfig',
    'recommend.apps.RecommendConfig',
    "room.apps.RoomConfig",
    'direct_messages.apps.DirectMessagesConfig',
]

CKEDITOR_UPLOAD_PATH = "uploads/"

#channels
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

#LEARN CHANNELS
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": ["redis://core-redis:6379"],
#         },
#     },
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #social
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                # custom context processors
                
           
                
              
            ],
            
        },
    },
]




# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env('POSTGRES_DB'),
#         'USER': env('POSTGRES_USER'),
#         'PASSWORD': env('POSTGRES_PASSWORD'),
#         'HOST': env('POSTGRES_HOST'),
#         'PORT': env('POSTGRES_PORT', default=5432),
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True 

USE_TZ = True

from django.utils.translation import gettext_lazy as _
gettext = lambda s: s
LANGUAGES = ( # Here
    ('ru', _('Russian')),
    ('en', _('English')),
    
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [ BASE_DIR / 'core' / 'static', ]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#crispy
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# email send

def email_verified_callback(user):
    user.is_active = True


# def password_change_callback(user, password):
#     user.set_password(password)


# Global Package Settings
EMAIL_FROM_ADDRESS = 'varvar1987a@gmail.com'  # mandatory
EMAIL_PAGE_DOMAIN = 'http://195.133.32.53:8000/'  # mandatory (unless you use a custom link)
#EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'
EMAIL_MULTI_USER = False  # optional (defaults to False)

# Email Verification Settings (mandatory for email sending)
EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
EMAIL_MAIL_HTML = 'account/email/mail_body.html'
EMAIL_MAIL_PLAIN = 'account/email/mail_body.txt'
EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# Email Verification Settings (mandatory for builtin view)
EMAIL_MAIL_PAGE_TEMPLATE = 'account/email/email_success_template.html'
EMAIL_MAIL_CALLBACK = email_verified_callback

# Password Recovery Settings (mandatory for email sending)
# EMAIL_PASSWORD_SUBJECT = 'Change your password {{ user.username }}'
# EMAIL_PASSWORD_HTML = 'password_body.html'
# EMAIL_PASSWORD_PLAIN = 'password_body.txt'
# EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# Password Recovery Settings (mandatory for builtin view)
# EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
# EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
# EMAIL_PASSWORD_CALLBACK = password_change_callback

# For Django Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'varvar1987a@gmail.com'
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # os.environ['password_key'] suggested
EMAIL_USE_TLS = True

#stripe
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_API_VERSION = env('STRIPE_API_VERSION')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET')

#yookassa
YOOKASSA_SECRET_KEY = env('YOOKASSA_SECRET_KEY')
YOOKASSA_SHOP_ID = env('YOOKASSA_SHOP_ID')

#google-fonts
GOOGLE_FONTS = ('Montserrat:wght@300;400', 'Roboto')
GOOGLE_FONTS_DIR = BASE_DIR / 'static'



# SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# SESSION_COOKIE_NAME = 'core_session_id'
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_COOKIE_AGE = 3600  # время в секундах 1 час



SITE_ID = 1
#Celery
#CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_BROKER_URL = 'redis://core-redis:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_CACHE_BACKEND = 'default'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True


#caches
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',#django_redis.cache.RedisCache #django.core.cache.backends.db.DatabaseCache
#         'LOCATION': 'redis://127.0.0.1:16379/1',
#     }
# }
# CELERY_BEAT_SCHEDULE = {
#     "sample_task": {
#         "task": "core.tasks.sample_task",
#         "schedule": crontab(minute="*/1"),
#         }
# }

# message tags
MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }





### social
#github
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2', #githube
    'social_core.backends.vk.VKOAuth2', #vk
    'django.contrib.auth.backends.ModelBackend'
)


SOCIAL_AUTH_VK_APP_USER_MODE = 2
#SOCIAL_AUTH_JSONFIELD_ENABLED = True 
SOCIAL_AUTH_GITHUB_KEY = env('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_URL_NAMESPACE = 'social'


#vk
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_VK_OAUTH2_KEY=env('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET=env('SOCIAL_AUTH_VK_OAUTH2_SECRET')
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/account/profile-management/'

#django-recaptcha
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE =  0,85 


#creditor
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',
            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

#

# User Modal
AUTH_USER_MODEL = 'account.User'

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
