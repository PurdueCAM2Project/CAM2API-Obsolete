"""
Django settings for API project.
Specific settings are imported other setting libraries for better
control. 
"""
from base_settings import *
import os

"""
This Below are the setting information for the production environment
CAM2API
"""

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '7t@@r3(twocu_9j+hawhl+m3#1$n9thgs7=jb%m!=w-ig!315*'

# # Allow all host headers
# ALLOWED_HOSTS = ['*']

# # Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# # Static asset configuration
# # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_ROOT = 'staticfiles'
# STATIC_URL = '/static/'

# STATIC_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
#     )

# # Default Set of DEBUG is False
# DEBUG = False




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
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = './API/static'

STATIC_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

# Default Set of DEBUG is False
DEBUG = True