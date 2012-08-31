import os
import sys

sys.path = ['/Library/Server/Web/Data/Sites/Default/DigitalLabels'] + sys.path
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'labelsite.settings'
application = WSGIHandler()


