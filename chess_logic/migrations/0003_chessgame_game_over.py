# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_logic', '0002_chessgame_turn'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessgame',
            name='game_over',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
