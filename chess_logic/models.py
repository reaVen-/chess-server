from __future__ import unicode_literals

from django.db import models

class ChessGame(models.Model):
	#all bricks
	ab = models.CharField(max_length=1000)

	#players
	player1_pk = models.CharField(max_length=10)
	player2_pk = models.CharField(max_length=10)

	#game state
	turn = models.CharField(max_length=1, default="w")
	game_over = models.CharField(max_length=1, default="0")

	#fields to assert game state
	pawn_over = models.BooleanField(default=False)
	white_king_moved = models.BooleanField(default=False)
	black_king_moved = models.BooleanField(default=False)
	white_tower_left_moved = models.BooleanField(default=False)
	white_tower_right_moved = models.BooleanField(default=False)
	black_tower_left_moved = models.BooleanField(default=False)
	black_tower_right_moved = models.BooleanField(default=False)
	

	
