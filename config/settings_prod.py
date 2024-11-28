import os

import dj_database_url
import environ

from .settings import *  # noqa

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

DATABASES = {'default': dj_database_url.config(conn_health_checks=True)}

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

CSRF_TRUSTED_ORIGINS = env('TRUSTED_ORIGINS').split(',')

SESSION_COOKIE_SECURE = True
CSRF_COOKIES_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ADMINS = [('Harouna', 'dev.harouna@gmail.com')]

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = '1000techleaders'
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_S3_ENDPOINT_FILES = env('AWS_S3_ENDPOINT_URL')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400'
}
AWS_DEFAULT_ACL = 'public-read'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
}

STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/tasks/static'

MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/tasks/media'

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3ManifestStaticStorage'
AWS_QUERYSTRING_AUTH = False


CSP_SCRIPT_SRC = [
    "'self'",
    "https://1000techleaders.fra1.digitaloceanspaces.com",
]
CSP_STYLE_SRC = [
    "'self'",
    "https://1000techleaders.fra1.digitaloceanspaces.com",
]
CSP_IMG_SRC = [
    "'self'",
    "https://1000techleaders.fra1.digitaloceanspaces.com",
]
CSP_FONT_SRC = [
    "'self'",
    "https://1000techleaders.fra1.digitaloceanspaces.com",
]
