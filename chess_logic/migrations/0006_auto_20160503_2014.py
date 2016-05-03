# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_logic', '0005_auto_20160429_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessgame',
            name='player1_pk',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chessgame',
            name='player2_pk',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chessgame',
            name='game_over',
            field=models.CharField(default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='chessgame',
            name='turn',
            field=models.CharField(default='w', max_length=1),
        ),
    ]
