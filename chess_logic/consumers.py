import json
from channels import Group
from channels.sessions import channel_session
from .models import ChessGame

@channel_session
def game_connect(message):
    prefix, label = message['path'].decode('ascii').strip("/").split("/")

    print "prefix: %s, label: %s"%(prefix, label)

    if prefix == "id" and label:
        Group('id-%s'%label, channel_layer=message.channel_layer).add(message.reply_channel)
        message.channel_session['game_id'] = label

@channel_session
def game_disconnect(message):
    print "someone disconnected"
    pass