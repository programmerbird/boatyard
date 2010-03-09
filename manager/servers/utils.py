
from django.conf import settings

from libcloud.types import Provider 
from libcloud.providers import get_driver 

def get_drivers():
	drivers = []
	for (service, args) in settings.CLOUD_ACCOUNTS:
		provider = getattr(Provider, service)
		driver = get_driver(provider)(*args)
		drivers.append(driver)
	return drivers
