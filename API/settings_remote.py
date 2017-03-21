"""
Django settings for API project.
Specific settings are imported other setting libraries for better
control. 
"""
import dj_database_url

"""
This Below are the setting information for the DEVELOPMENT environment
CAM2API
"""
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7t@@r3(twocu_9j+hawhl+m3#1$n9thgs7=jb%m!=w-ig!315*'

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Using white noise to collect static files on production
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage' 

# # More Static File Collection
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
#     )

# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Heroku Database
DATABASES = {
    'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
}
# Add PostGIS engine
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Default Set of DEBUG is False
DEBUG = True