import json
from channels import Group
from channels.sessions import channel_session

def home_connect(message):
    prefix, label = message['path'].decode('ascii').strip("/").split("/")

    print "home -- prefix: %s, label: %s"%(prefix, label)

    Group("user-%s" % label, channel_layer=message.channel_layer).add(message.reply_channel)

def home_disconnect(message):
    print "home disconnect"