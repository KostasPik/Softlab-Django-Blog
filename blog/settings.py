"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ThisIsSupposedToBeTopSecret!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
 
    #my apps begin
        'posts',
        'newsletter',
        'accounts',
    # my apps end


    #dependencies apps begin

    'ckeditor',
    'ckeditor_uploader',
    'pyuploadcare.dj',
    'django.contrib.postgres',
    'crispy_forms',
    'compressor',
    #dependencies apps end

    "debug_toolbar",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.gzip.GZipMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",


    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'posts.context_processors.get_tags',
                'posts.context_processors.newsletter_form',
                'posts.context_processors.feedback_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# STATIC FILES COMPRESSION BEGIN

COMPRESS_ROOT = '/static/'
COMPRESS_ENABLED = False 
COMPRESS_STORAGE = 'compressor.storage.BrotliCompressorFileStorage' # use brotli compression to compress the response as much as possible.

COMPRESS_CACHE_BACKEND = 'default'
COMPRESS_OFFLINE = True
# STATIC FILES COMPRESSION END


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# EXTRA SETTING BEGIN

UPLOADCARE = {
    'pub_key': 'UPLOADCARE_PUBLIC_KEY', # UPLOADCARE keys for the the image CDN
    'secret': 'UPLOADCARE_SECRET_KEY',
}

# RICH TEXT EDITOR BEGIN 
CKEDITOR_UPLOAD_PATH = 'ckeditor/uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'width':'100%',
        'extraPlugins': ['codesnippet','uploadcare'],
        'toolbar': 'full',  # put selected toolbar config here
        'tabSpaces': 4,
        'uploadcare': {'publicKey': UPLOADCARE['pub_key']}
    },
}
# RICH TEXT EDITOR END 


#STRIPE API KEY TO ACCEPT DONATIONS (Buy me a coffee...)
STRIPE_API_KEY="STRIPE SECRET API KEY"


# bootstrapify login/ signup form with django
CRISPY_TEMPLATE_PACK = 'bootstrap4'


#EMAIL SETUP BEGIN
EMAIL_HOST = 'EMAIL HOST'
EMAIL_USE_TLS = True
EMAIL_PORT = 587

EMAIL_HOST_USER = 'EMAIL USERNAME' # email 
EMAIL_HOST_PASSWORD = 'EMAIL PASSWORD'# email password
#EMAIL SETUP END

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://redis-14806.c267.us-east-1-4.ec2.cloud.redislabs.com:14806",
#         "OPTIONS": {
#             'PASSWORD': 'FLZ9NiHVY9FvW03S2GzaBJpI7F46ZlCb',
#         },
#     }
# }

CACHE_TTL = 60 * 1 #Caching timeout

#USER MODEL FOR AUTHENTICATION (OUR OWN CUSTOM MODEL)
AUTH_USER_MODEL = "accounts.CustomUser"
AUTHENTICATION_BACKENDS = ["accounts.backend.CustomUserModelBackend"]

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'



from django.contrib.messages import constants as messages


MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }


SITE_ID = 1
#EXTRA SETTINGS END