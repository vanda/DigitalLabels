import os
import sys

sys.path = ['/usr/share/pyshared'] + sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'labelsite.settings_amazon'
application = WSGIHandler()

