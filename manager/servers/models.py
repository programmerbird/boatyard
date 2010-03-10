#-*- coding:utf-8 -*-

from django import forms
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils import simplejson as json
from libcloud.types import Provider as LibCloudProvider


SSH = -1
class RackspaceProvider (forms.Form):
	name = forms.CharField(label='Provider name')
	
	username = forms.CharField()
	api_key = forms.CharField()
	
	def get_name(self):
		return self.data['name']
		
	class Meta:
		name = 'Rackspace'
		pk = LibCloudProvider.RACKSPACE
		
class SSHProvider (forms.Form):
	name = forms.CharField(label='Provider name')
	
	username = forms.CharField(initial='root')
	public_ip = forms.CharField()
	private_ip = forms.CharField(required=False)
	
	def get_name(self):
		return self.data['name']
		
	class Meta:
		name = 'SSH'
		pk = SSH
		

PROVIDERS = [
	SSHProvider,
	RackspaceProvider,
]
PROVIDERS_MAP = dict([ (x.Meta.pk, x) for x in PROVIDERS ])
PROVIDERS_CHOICES = [ (x.Meta.pk, x.Meta.name) for x in PROVIDERS ]

class Provider (models.Model):
	name = models.CharField(verbose_name="Provider name", max_length=200)
	provider = models.IntegerField(choices=PROVIDERS_CHOICES)
	storage = models.TextField()
	
	def set_form(self, form):
		self.pk = getattr(form, 'pk', None)
		self.name = form.get_name()
		self.provider = form.Meta.pk 
		self.storage = json.dumps(form.data)
		
	def get_form(self):
		form_cls = PROVIDERS_MAP[self.provider]
		form = form_cls(data=json.loads(self.storage))
		form.pk = self.pk
		return form 

