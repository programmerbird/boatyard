#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *


class NodeForm (forms.ModelForm):
	class Meta:
		model = Node

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		node = None
		if args:
			name = args[0]
			args = args[1:]
			try:
				node = Node.by_name(name)
			except Node.DoesNotExist:
				pass 
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
				pass
			else:
				form = NodeForm(instance=node)
				form = edit_form(form)
				form.save(commit=True)
		
