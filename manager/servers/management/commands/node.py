#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *
from fabric.api import *

class ServiceNotInstalled(Exception):
	pass 

	
def dispatch(node, service_args):
	import services 
	service_name = service_args[0]
	service_args = service_args[1:]
	
	__import__('services.' + service_name)
	service = getattr(services, service_name)
	installed_services = json.loads(node.services or '[]')
	
	if getattr(service, 'NEED_INSTALLED', False):
		if not service_name in installed_services:
			raise ServiceNotInstalled("%s require installation" % service_name)
	
	# check 
	if not getattr(service, 'HANDLE_ARGS', False):
		for arg in service_args:
			if arg.startswith('_'):
				raise AttributeError(arg)
			getattr(service, arg)	
	
	# run 
	env.node = node
	if not getattr(service, 'HANDLE_ARGS', False):
		service.init()
		for arg in service_args:
			getattr(service, arg)()
	else:
		service.init(*service_args)
	
class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		node = None
		if args:
			name = args[0]
			args = args[1:]
			try:
				node = Node.by_name(name)
			except Node.DoesNotExist:
				args = [name] + args
		if not node:
			print "Please select node below:"
			nodes = []
			providers = Provider.objects.all()
			for provider in providers:
				for node in provider.get_driver().list_nodes():
					Node.get(provider, node.name)
					
			nodes = Node.objects.order_by('name')
			node = menu([ (node, unicode(node)) for node in nodes ])
		if node:
			if args:
				# run service 
				try:
					dispatch(node, args)
					return
				except ImportError, e:
					print e 
				except AttributeError, e:
					print e
					dispatch(node, ['help', args[0]])
					return 
				except ServiceNotInstalled, e:
					return 
				except:
					import traceback
					traceback.print_exc()
					return
			
			dispatch(node, ['help',])
			

