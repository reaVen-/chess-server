import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import ChessGame, Room

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    prefix, label = message['path'].decode('ascii').strip("/").split("/")

    print "prefix: %s, label: %s"%(prefix, label)

    if prefix == "id" and label:
        Group('id-%s'%label, channel_layer=message.channel_layer).add(message.reply_channel)
        message.channel_session['game_id'] = label

@channel_session
def ws_receive(message):
    #is not used at the moment
    Group("id-"+message.channel_session['game_id']).send({'text':json.dumps({'foo':'bar'})})

@channel_session
def ws_disconnect(message):
    pass