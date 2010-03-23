#-*- coding:utf-8 -*-

from django import forms
from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django.utils import simplejson as json 
from servers.console import menu, new_form, edit_form
from servers.models import *

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		form = None
		if len(args) != 2:
			raise Exception("Usage: boatyard provider-mv [name] [new-name]")
		name = args[0]
		new_name = args[1]
		
		try:
			provider = Provider.objects.get(name=name)
		except Provider.DoesNotExist:
			raise Exception("[%s] does not exists" % name)
		if Provider.objects.filter(name=new_name):
			raise Exception("[%s] alread existed" % new_name)
			
		provider.name = new_name
		provider.save()

