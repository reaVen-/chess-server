# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-04 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_logic', '0007_auto_20160503_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chessgame',
            name='turn',
            field=models.CharField(default='hvit', max_length=5),
        ),
    ]
