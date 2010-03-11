#-*- coding:utf-8 -*-


from fabric.api import *
from django.utils import simplejson as json 
from servers.models import Node 
from servers.utils import get_service, get_services
import os 


HANDLE_ARGS = True

def init(*args):
	print ""
	if not args:
		print "Available Services"
	
		installed_services = json.loads(env.node.services or '[]')
		if installed_services:
			for x in installed_services:
				print "-", x, "[installed]"
		
		for (service_name, path, options) in get_services():
			if options['NEED_INSTALLED']:
				continue
			print '-', service_name
		print ''
	else:
		service_name = args[0]
		service = get_service(service_name)
		print service.__doc__

