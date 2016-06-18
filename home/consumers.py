import json
from channels import Group
from channels.sessions import channel_session

def home_connect(message):
	print message['path']

def home_disconnect(message):
	pass