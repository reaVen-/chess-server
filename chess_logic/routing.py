from channels.routing import route

from .consumers import send_move, get_move

channel_routing = [
    route('send-move',send_move),
    route('get-move', get_move),
]