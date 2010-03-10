#-*- coding:utf-8 -*-

from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django import forms
from servers.console import menu, new_form, edit_form
from servers.models import *


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		provider = None
		if not provider:
			print "Please select provider below:"
			provider = menu([
				(x, unicode(x)) for x in Provider.objects.all() 
			])
		if provider:
			provider.delete()

