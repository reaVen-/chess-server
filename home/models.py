from __future__ import unicode_literals

from django.db import models

class ChessUser(models.Model):
	username = models.CharField(max_length=10, unique=True)
	password = models.CharField(max_length=255)