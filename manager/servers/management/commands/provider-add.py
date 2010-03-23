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
		if not args:
			raise Exception("Usage: boatyard provider-add [name]")
		name = args[0]
		if Provider.objects.filter(name=name):
			raise Exception("[%s] alread existed" % name)
			
		print "Please select driver below:"
		form = menu([
			(x(), x.Meta.slug) for x in DRIVERS 
		])
		form = new_form(form)
		p = Provider()
		p.name = name 
		p.driver = getattr(types, form.Meta.slug)
		p.storage = json.dumps(form.data)
		p.save()
		
