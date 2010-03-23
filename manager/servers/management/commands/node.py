#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *
from servers.utils import get_service 
from fabric.api import *

class ServiceNotInstalled(Exception):
	pass 

	
def dispatch(node, service_args):
	service_name = service_args[0]
	service_args = service_args[1:]
	
	service = get_service(service_name)
	if service.NEED_INSTALLED and not service_name in installed_services:
		raise ServiceNotInstalled("%s require installation" % service_name)
	
	# check 
	if not service.HANDLE_ARGS:
		for arg in service_args:
			if arg.startswith('_'):
				raise AttributeError(arg)
			getattr(service, arg)	
	
	# run 
	env.node = node
	if not service.HANDLE_ARGS:
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
			nodes = []
			providers = Provider.objects.all()
			for provider in providers:
				for node in provider.get_driver().list_nodes():
					Node.get(provider, node.name)
					
			nodes = Node.objects.order_by('name')
			for node in nodes:
				print node
			return 
		if node:
			if args:
				# run service 
				try:
					dispatch(node, args)
					exit(0)
					return
				except ImportError, e:
					print e 
				except AttributeError, e:
					print e
					dispatch(node, ['help', args[0]])
					exit(0)
					return 
				except ServiceNotInstalled, e:
					exit(0)
					return 
				except SystemExit:
					exit(0)
				except:
					import traceback
					traceback.print_exc()
					exit(0)
					return
			dispatch(node, ['help',])
			exit(0)
			

