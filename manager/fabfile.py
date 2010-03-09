
from fabric.api import *

env.hosts = ['127.0.0.1']

def setup():
	local('virtualenv --no-site-packages env')
	local('env/bin/pip install -r requirements.ini')
