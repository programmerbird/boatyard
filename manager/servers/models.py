#-*- coding:utf-8 -*-

from django import forms
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils import simplejson as json
from libcloud.types import Provider as types
from libcloud.providers import get_driver

class RackspaceDriver (forms.Form):
	username = forms.CharField()
	api_key = forms.CharField()
	class Meta:
		slug = 'RACKSPACE'
		fields = ('username', 'api_key',)

class SlicehostDriver (forms.Form):
	api_key = forms.CharField()
	class Meta:
		slug = 'SLICEHOST'
		fields = ('api_key',)


class EC2Driver (forms.Form):
	access_key_id = forms.CharField()
	secret_key = forms.CharField()
	class Meta:
		slug = 'EC2'
		fields = ('access_key_id', 'secret_key',)


DRIVERS = [
	EC2Driver,
	SlicehostDriver,
	RackspaceDriver,
]

DRIVERS_MAP = dict([ (getattr(types, x.Meta.slug), x) for x in DRIVERS ])
DRIVERS_CHOICES = [ (getattr(types, x.Meta.slug), x.Meta.slug) for x in DRIVERS ]

class Provider (models.Model):
	driver = models.IntegerField(choices=DRIVERS_CHOICES)
	storage = models.TextField()
	
	def get_storage(self):
		try:
			return self._storage
		except AttributeError:
			self._storage = s = json.loads(self.storage)
			return s 
			
	def get_driver(self):
		try:
			return self._driver 
		except AttributeError:
			fields = DRIVERS_MAP[self.driver].Meta.fields
			storage = self.get_storage()
			args = [ storage[x] for x in fields ]
			self._driver = d = get_driver(self.driver)(*args)
			return d 
			
	def get_driver_name(self):
		return DRIVERS_MAP[self.driver].Meta.slug
			
	def __unicode__(self):
		return self.get_driver_name() + ' ' + self.storage



class Node(models.Model):
	name = models.CharField(max_length=200)
	provider = models.ForeignKey(Provider, null=True, editable=False)
	services = models.TextField(null=True, blank=True, editable=False)
	storage = models.TextField(null=True, blank=True, editable=False)
	
	username = models.CharField(max_length=200, default='root')
	public_ip = models.TextField(null=True, blank=True)
	private_ip = models.TextField(null=True, blank=True)
	
	def get_public_ip(self):
		if not self.provider:
			return json.loads(self.public_ip)
		else:
			conn = self.get_connection()
			return conn.public_ip
			
	def get_storage(self):
		try:
			return self._storage
		except AttributeError:
			self._storage = s = json.loads(self.storage)
			return s 
				
	def get_service_storage(self, service):
		return self.get_storage().get(service, {})
		
	def set_service_storage(self, service, value):
		self.get_storage()[service] = value 
		
	def get_private_ip(self):
		if not self.provider:
			return json.loads(self.private_ip)
		else:
			conn = self.get_connection()
			return conn.private_ip
					
	def get_connection(self):
		try:
			return self._conn
		except:
			if self.provider:
				driver = self.provider.get_driver()
				for x in driver.list_nodes():
					if x.name == self.name:
						self._conn = x 
						return x 
			self._conn = None
		
	@classmethod 
	def get(self, provider, name):
		return Node.objects.get_or_create(provider=provider, name=name)
		
	@classmethod 
	def by_name(self, name):
		try:
			return Node.objects.get(name=name)
		except Node.DoesNotExist:
			providers = Provider.objects.all()
			for provider in providers:
				nodes = provider.get_driver().list_nodes()
				for node in nodes:
					if node.name == name:
						return Node.get(provider, name)
			raise Node.DoesNotExist
			
	def save(self, *args, **kwargs):
		if hasattr(self, '_storage'):
			self.storage = json.dumps(self._storage)
		if self.public_ip and not self.public_ip.startswith('['):
			self.public_ip = json.dumps([self.public_ip])
		if self.private_ip and not self.private_ip.startswith('['):
			self.private_ip = json.dumps([self.private_ip])
		super(Node, self).save(*args, **kwargs)
			
	def __unicode__(self):
		if self.provider:
			return self.name + ' [ ' + self.provider.get_driver_name() + ' ] '
		else:
			return self.name
		

		
