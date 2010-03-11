#-*- coding:utf-8 -*-


from fabric.api import *
from django.utils import simplejson as json 
from servers.models import Node 

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
				
		import services
		service_names = []
		with hide('running', 'stdout', 'stderr'):
			file_names = local('ls ' + os.path.dirname(__file__) + '/*.py').split()
		for file_name in file_names:
			file_name = file_name.rsplit(os.sep,1)[-1].strip()[:-3]
			if not file_name:
				continue 
			if file_name.startswith('_'):
				continue
			service_names.append(file_name)
		
		service_names.sort()
		for x in service_names:
			__import__('services.' + x)
			service = getattr(services, x)
			if getattr(service, 'NEED_INSTALLED', False):
				continue 
			print "-", x
		print ""
	else:
		service_name = args[0]
		import services 
		__import__('services.' + service_name)
		service = getattr(services, service_name)
		print service.__doc__

