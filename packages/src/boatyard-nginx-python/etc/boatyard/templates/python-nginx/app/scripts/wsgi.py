import os,sys

sys.path.append('/home/{{BOATYARD_USER}}/deployed-apps/{{BOATYARD_APP}}/webs/')
sys.path.append('/home/{{BOATYARD_USER}}/deployed-apps/{{BOATYARD_APP}}/')

os.environ['DJANGO_SETTINGS_MODULE'] = '{{BOATYARD_APP}}{{BOATYARD_RANDOM}}.settings_{{BOATYARD_CONFIG}}'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

