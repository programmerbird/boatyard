#-*- coding:utf-8 -*-

from django import forms
from django.core.management.base import NoArgsCommand, BaseCommand
from django.db.models.query_utils import CollectedObjects
from django.utils import simplejson as json 
from servers.console import menu, new_form, edit_form
from keys.models import *
from keys import forms 

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		form = None
		if not args:
			print "Usage: boatyard publickey-add [name] < ~/.ssh/id_rsa.pub"
			return 
		name = args[0]
		if PublicKey.objects.filter(name=name):
			print "[%s] already existed" % name
			return
		
		import sys 
		content = ''.join(sys.stdin.readlines())
		if content:
			n = PublicKey()
			n.name = name 
			n.content = content 
			n.save()
		else:
			print "no key specific"
