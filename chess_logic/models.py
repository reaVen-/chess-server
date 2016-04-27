from __future__ import unicode_literals

from django.db import models

class ChessGame(models.Model):
	ab = models.CharField(max_length=1000)
	turn = models.CharField(max_length=1)
	game_over = models.CharField(max_length=1)
	pawn_over = models.BooleanField(default=False)
	
