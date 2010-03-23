#-*- coding:utf-8 -*-
"""
Install SSH Public Key

usage: 

boatyard node [nodename] authorized_keys add [keyname] to [username] 
boatyard node [nodename] authorized_keys add [keyname] // username==keyname

"""

from fabric.api import *
from fabric.contrib.files import exists
from django import forms
from servers.console import menu
from keys.models import PublicKey

HANDLE_ARGS = True

def init(*args):
	env.user = 'root'
	env.password = env.node.get_password()
	env.host_string = 'root@%s' % env.node.get_public_ip()[0]

	if args[0] == 'add':
		return add(*args[1:])

	raise AttributeError
		
def add(*args):
	if len(args) not in (1,3):
		raise AttributeError
		
	publickey = PublicKey.objects.get(name=args[0])
	username = args[-1]
	
	if username=='root':
		env.home = '/root'
	else:
		env.home = '/home/%s' % username 

	if not exists(env.home):
		raise Exception("User [%s] does not exists" % username)
		
	env.tmp_file = '/tmp/publickey.tmp' 
	f = open(env.tmp_file, 'w')
	f.write(publickey.content)
	f.close()

	put(env.tmp_file, env.tmp_file)
	local('rm %(tmp_file)s' % env)

	run('mkdir -p %(home)s/.ssh' % env, pty=True)
	run('cat %(tmp_file)s >> %(home)s/.ssh/authorized_keys' % env, pty=True)
	
	print "remove duplicate entries.."
	with hide('running', 'stdout', 'stderr'):
		run('cat %(home)s/.ssh/authorized_keys | sort | uniq > %(tmp_file)s' % env, pty=True)
		run('mv %(tmp_file)s %(home)s/.ssh/authorized_keys' % env, pty=True)


