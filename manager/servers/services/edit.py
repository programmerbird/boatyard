#-*- coding:utf-8 -*-
"""
Edit node information

usage: boatyard node [nodename] edit
"""

from fabric.api import *
from django import forms
from servers.console import edit_form
from servers.models import Node 

class NodeForm (forms.ModelForm):
	class Meta:
		model = Node

def init():
	form = NodeForm(instance=env.node)
	form = edit_form(form)
	form.save(commit=True)
	print "saved", env.node

