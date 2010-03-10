#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		form = None
		if args:
			provider = args[0]
			for x in PROVIDERS:
				if x.Meta.name.lower() == provider.lower():
					form = x()
		if not form:
			print "Please select provider below:"
			form = menu([
				(x(), x.Meta.name) for x in PROVIDERS 
			])
		form = new_form(form)
		p = Provider()
		p.set_form(form)
		p.save()
		
