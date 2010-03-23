#-*- coding:utf-8 -*-

from django import forms
from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django.utils import simplejson as json 
from servers.console import menu, new_form, edit_form
from keys.models import *

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if len(args) != 1:
			raise Exception("Usage: boatyard publickey-rm [name]")
		name = args[0]
		try:
			publickey = PublicKey.objects.get(name=name)
		except PublicKey.DoesNotExist:
			raise Exception("[%s] does not exists" % name)
		publickey.delete()

