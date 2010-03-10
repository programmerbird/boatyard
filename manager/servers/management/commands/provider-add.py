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
		if args:
			driver = args[0]
			for x in DRIVERS:
				if x.Meta.slug.lower() == driver.lower():
					form = x()
		if not form:
			print "Please select driver below:"
			form = menu([
				(x(), x.Meta.slug) for x in DRIVERS 
			])
		form = new_form(form)
		p = Provider()
		p.driver = getattr(types, form.Meta.slug)
		p.storage = json.dumps(form.data)
		p.save()
		
