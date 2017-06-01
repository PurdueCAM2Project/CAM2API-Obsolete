"""
Django settings for API project.
Specific settings are imported other setting libraries for better
control. 
"""
import dj_database_url
import os

print("Imported Remote Settings......")

"""
This Below are the setting information for the DEVELOPMENT environment
CAM2API
"""
# Root Project Directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
# To add secret key variable to Heroku Deployment use "heroku config:add DJANGO_SECRET_KEY=<your secret key>" 
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/staticfiles/'

# Using white noise to collect static files on production
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage' 

# # More Static File Collection
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
#     )

# Ensures all API requests are directed through HTTPS
# SECURE_SSL_REDIRECT = True

# Get geoDjango GEOS and GDAL library paths from Heroku environment variables
GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')


# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# Heroku Database
DATABASES = {
    'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
}
# Add PostGIS engine
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Default Set of DEBUG is False
DEBUG = True

# Ensures all API requests are directed through HTTPS
# SECURE_SSL_REDIRECT = True