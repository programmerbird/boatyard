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
from servers.console import menu
from keys.models import PublicKey

HANDLE_ARGS = True

def init(*args):
	env.user = 'root'
	env.password = env.node.get_password()
	env.host_string = 'root@%s' % env.node.get_public_ip()[0]

	cmd = args[0]
	if cmd == 'add':
		return add(*args[1:])

	raise AttributeError
		
def add(*args):
	if len(args) not in (1,3):
		raise AttributeError
		
	publickey = PublicKey.objects.get(name=args[0])
	env.keyuser = args[-1]
	
	if username=='root':
		env.home = '/root'
	else:
		env.home = '/home/%s' % username 

	if not exists(env.home):
		raise Exception("User [%s] does not exists" % username)

	run('mkdir -p %(home)s/.ssh' % env, pty=True)
	
	keys = publickey.content.split('\n')
	append(keys, '%(home)s/.ssh/authorized_keys')
	run('chown -R %(keyuser)s:%(keyuser)s %(home)s/.ssh/', pty=True)

