#-*- coding:utf-8 -*-
"""
Install SSH Public Key

usage: 

boatyard node [nodename] authorized_keys add [keyname] to [username] 
boatyard node [nodename] authorized_keys add [keyname] // username==keyname

"""
from boatyard.services import *
from keys.models import PublicKey

ADMIN_USER = getattr(settings, 'ADMIN_USER', 'root')
ADMIN_PUBLICKEY_NAME = getattr(settings, 'ADMIN_PUBLICKEY_NAME', ADMIN_USER)

def install(*args):
	connect()
	
	env.admin_user = ADMIN_USER
	env.public_key = ADMIN_PUBLICKEY_NAME
	manage("authorized_keys add %(public_key)s to %(admin_user)s" % env)
		
	print "Adding Boatyard Repository.."
	append('deb http://boatyard.s3.amazonaws.com/repositories/debian binary/', '/etc/apt/sources.list')
	run('gpg --keyserver keyserver.ubuntu.com --recv-keys 9CE8C487', pty=True)
	run('gpg -a --export 9CE8C487 | sudo apt-key add -', pty=True)
	
	print "Updating server.."
	run('aptitude update', pty=True)
	run('aptitude -y safe-upgrade', pty=True)
	
def installkey():
	connect()
	
	print "Adding Boatyard Repository.."
	append('deb http://boatyard.s3.amazonaws.com/repositories/debian binary/', '/etc/apt/sources.list')
	run('gpg --keyserver keyserver.ubuntu.com --recv-keys 9CE8C487', pty=True)
	run('gpg -a --export 9CE8C487 | sudo apt-key add -', pty=True)
	
