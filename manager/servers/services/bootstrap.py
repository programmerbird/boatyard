#-*- coding:utf-8 -*-
"""
Install SSH Public Key

usage: 

boatyard node [nodename] authorized_keys add [keyname] to [username] 
boatyard node [nodename] authorized_keys add [keyname] // username==keyname

"""

from fabric.api import *
from fabric.contrib.files import exists, append
from django import forms
from django.conf import settings 
from servers.console import menu
from keys.models import PublicKey

HANDLE_ARGS = True
ADMIN_USER = getattr(settings, 'ADMIN_USER', 'bird')
ADMIN_PUBLICKEY_NAME = getattr(settings, 'ADMIN_PUBLICKEY_NAME', ADMIN_USER)

def add_admin_user():
	if not exists(env.home):
		run("yes '' | adduser --home %(home)s --disabled-password %(admin_user)s" % env, pty=True)
	try:
		publickey = PublicKey.objects.get(name=ADMIN_PUBLICKEY_NAME)
	except PublicKey.DoesNotExist:
		return
		
	keys = publickey.content.split('\n')
	run('mkdir -p %(home)s/.ssh' % env, pty=True)
	append(keys, '%(home)s/.ssh/authorized_keys' % env)
	run('chown -R %(admin_user)s:%(admin_user)s %(home)s/.ssh' % env, pty=True)

def init(*args):
	print "Resetting Root Password.."
	env.user = 'root'
	env.password = env.node.get_password()
	env.host_string = 'root@%s' % env.node.get_public_ip()[0]
	
	env.admin_user = ADMIN_USER
	if env.admin_user=='root':
		env.home = '/root'
	else:
		env.home = '/home/%s' % env.admin_user 
	
	print "Adding %s User.." % ADMIN_USER
	add_admin_user()
		
	print "Adding Boatyard Repository.."
	append('deb http://boatyard.s3.amazonaws.com/repositories/debian binary/', '/etc/apt/sources.list')
	run('gpg --keyserver keyserver.ubuntu.com --recv-keys 9CE8C487', pty=True)
	run('gpg -a --export 9CE8C487 | sudo apt-key add -', pty=True)
	
	print "Updating server.."
	run('aptitude update', pty=True)
	run('aptitude -y safe-upgrade', pty=True)
