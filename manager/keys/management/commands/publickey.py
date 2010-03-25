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
		if not args:
			for x in PublicKey.objects.all().order_by('name'):
				print unicode(x)
			return 
			
		name = args[0] 
		if name in ('add', 'mv', 'rm'):
			return getattr(self, name)(*args[1:])
			
		try:
			publickey = PublicKey.objects.get(name=name)
			print publickey.content
		except PublicKey.DoesNotExist:
			pass
			
	def add(self, *args, **kwargs):
		form = None
		if not args:
			print "Usage: boatyard publickey add [name] < ~/.ssh/id_rsa.pub"
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
			
	def mv(self, *args, **kwargs):
		if len(args) != 2:
			print "Usage: boatyard publickey mv [name] [new-name]"
			return
		name = args[0]
		new_name = args[1]
		
		try:
			publickey = PublicKey.objects.get(name=name)
		except PublicKey.DoesNotExist:
			raise Exception("[%s] does not exists" % name)
		if PublicKey.objects.filter(name=new_name):
			raise Exception("[%s] alread existed" % new_name)
			
		publickey.name = new_name
		publickey.save()

	def rm(self, *args, **kwargs):
		if len(args) != 1:
			print "Usage: boatyard publickey rm [name]"
			return 
		name = args[0]
		
		try:
			publickey = PublicKey.objects.get(name=name)
		except PublicKey.DoesNotExist:
			raise Exception("[%s] does not exists" % name)
		publickey.delete()

			
