#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from keys.models import *
from keys import forms

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		publickey = None
		if args:
			name = args[0] 
			try:
				publickey = PublicKey.objects.get(name=name)
			except PublicKey.DoesNotExist:
				pass
		if publickey:
			print publickey.content
			return 
		for x in PublicKey.objects.all().order_by('name'):
			print unicode(x)
