from __future__ import unicode_literals

from django.db import models

class ChessUser(models.Model):
	username = models.CharField(max_length=15, unique=True)
	password = models.CharField(max_length=255)

class Challenge(models.Model):
	player1 = models.ForeignKey(ChessUser, on_delete=models.CASCADE, related_name="challenger")
	player2 = models.ForeignKey(ChessUser, on_delete=models.CASCADE, related_name="opponent")
