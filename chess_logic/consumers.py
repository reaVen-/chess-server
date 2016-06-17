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
    data = json.loads(message['text'])

    print "prefix: %s, label: %s"%(prefix, label)
    print data

    if prefix == "id" and label:
        Group('id-%s'%label, channel_layer=message.channel_layer).add(message.reply_channel)
        message.channel_session['game_id'] = label

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    print "RECEIVED MESSAGE"

    data = json.loads(message['text'])
    print data

    """
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
    except KeyError:
        log.debug('no room in channel_session')
        return
    except Room.DoesNotExist:
        log.debug('recieved message, buy room does not exist label=%s', label)
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s', 
            room.label, data['handle'], data['message'])
        m = room.messages.create(**data)

        # See above for the note about Group
        Group('chat-'+label, channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})
    """

@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-'+label, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass