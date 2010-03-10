
from django.conf import settings

from libcloud.types import Provider 
from libcloud.providers import get_driver 


DRIVERS = dict([ (name, (service, args)) for (name,service, args) in settings.CLOUD_ACCOUNTS ])

def get_drivers():
	drivers = []
	for (name, (service, args)) in DRIVERS.items():
		provider = getattr(Provider, service)
		driver = get_driver(provider)(*args)
		drivers.append(driver)
	return drivers
	
