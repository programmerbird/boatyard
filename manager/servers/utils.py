#-*- coding:utf-8 -*-

from django.db.models import get_apps
import os 

COMMON_ARGS = (
	('HANDLE_ARGS', False),
	('NEED_INSTALLED', False),
)

SERVICES = [
	#('name', 'module.path', {'HANDLE_ARGS': True}),
]

def get_app_services(app):
	result = []
	handles = []
	services_path = os.path.join(os.path.dirname(app.__file__), 'services')
	if os.path.exists(services_path):
		for file_name in os.listdir(services_path):
			if file_name.endswith('~'):
				continue
			if file_name.startswith('__'):
				continue
			if not (file_name.endswith('.pyc') or file_name.endswith('.py')):
				continue 
			service_name = file_name.rsplit('.', 1)[0]
			if service_name in handles:
				continue 
			handles.append(service_name)
			service_def = app.__package__ + '.services.' + service_name
			service = load_module(service_def)
			opts = dict([ (x, getattr(service, x, default)) for (x, default) in COMMON_ARGS ])
			result.append( (service_name, service_def, opts), )
	return result
		
	
def get_services():
	global SERVICES
	if SERVICES:
		return SERVICES
	else:
		result = []
		for app in get_apps():
			app_services = get_app_services(app)
			if app_services:
				for service in app_services:
					result.append(service)
		SERVICES = result 
		return result


def load_module(definition):
	module = __import__(definition)	
	components = definition.split('.')
	for component in components[1:]:
		module = getattr(module, component)
	return module
	
def get_service(name):
	for (service_name, path, options) in get_services():
		if name != service_name:
			continue
		service = load_module(path) 
		for k,v in options.items():
			setattr(service, k, v)
		return service 
