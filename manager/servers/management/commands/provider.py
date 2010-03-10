#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		provider = None
		if args:
			name = args[0]
			try:
				provider = Provider.objects.get(name=name)
			except Provider.DoesNotExist:
				pass
		if not provider:
			print "Please select provider below:"
			provider = menu([
				(x, x.name) for x in Provider.objects.all() 
			])
			
		form = provider.get_form()
		form = edit_form(form)
		provider.set_form(form)
		provider.save()
		
