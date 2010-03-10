#-*- coding:utf-8 -*-

from django.db import models
from django.db.models import signals
from django.conf import settings

from libcloud.types import Provider

PROVIDERS = (
	(-1, 'SSH'),
	(Provider.RACKSPACE, 'RACKSPACE'),
)

class Account (models.Model):
	name = models.CharField(verbose_name="Account name", max_length=200)
	provider = models.IntegerField(choices=PROVIDERS)
	storage = models.TextField()
	

