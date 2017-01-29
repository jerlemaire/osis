# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-24 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0002_auto_20160623_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='dissertation',
            name='defend_periode',
            field=models.CharField(choices=[('UNDEFINED', 'undefined'), ('JANUARY', 'January'), ('JUIN', 'Juin'), ('SEPTEMBER', 'September')], default='UNDEFINED', max_length=12),
        ),
    ]