from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class ChessGame(models.Model):
	#all bricks
	ab = models.CharField(max_length=1000)

	#players
	player_white_pk = models.CharField(max_length=10)
	player_black_pk = models.CharField(max_length=10)

	#game state
	turn = models.CharField(max_length=5, default="hvit")
	game_over = models.CharField(max_length=1, default="0")

	#fields to assert game state
	pawn_over = models.BooleanField(default=False)
	white_king_moved = models.BooleanField(default=False)
	black_king_moved = models.BooleanField(default=False)
	white_tower_left_moved = models.BooleanField(default=False)
	white_tower_right_moved = models.BooleanField(default=False)
	black_tower_left_moved = models.BooleanField(default=False)
	black_tower_right_moved = models.BooleanField(default=False)

	#stockfish working on this game
	looking_for_move = models.BooleanField(default=False)

class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
    
    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}
