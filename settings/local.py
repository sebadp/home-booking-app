from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['testserver', 'localhost', '0.0.0.0']



# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'new_project_db_1',
        'PORT': 5432,
        'TEST': {
            'NAME': 'testing_db',
        },
    }
}


