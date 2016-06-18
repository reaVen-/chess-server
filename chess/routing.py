from chess_logic.consumers import game_connect, game_disconnect
from home.consumers import home_connect, home_disconnect
from channels.routing import route, include

game_routing = [
	route("websocket.connect": game_connect),
	route("websocket.disconnect": game_disconnect),

]

home_routing = [
	route("websocket.connect": home_connect),
	route("websocket.disconnect": home_disconnect),
]

routing = [
	include(game_routing, path=r"^/id/"),
	include(home_routing, path=r"^/user/"),
]