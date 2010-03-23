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
			provider_name = args[0] 
			try:
				provider = Provider.objects.get(name=provider_name)
			except Provider.DoesNotExist:
				pass
		if not provider:
			for x in Provider.objects.all().order_by('name'):
				print unicode(x)
			return 
			
		if provider:
			form = DRIVERS_MAP[provider.driver](data=json.loads(provider.storage))
			form = edit_form(form)
			provider.storage = json.dumps(form.data)
			provider.save()
		
