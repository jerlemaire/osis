# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-26 07:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0137_auto_20170620_1042'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='learningunit',
            options={'permissions': (('can_access_learningunit', 'Can access learning unit'), ('can_edit_learningunit_pedagogy', 'Can edit learning unit pedagogy'), ('can_edit_learningunit_specification', 'Can edit learning unit specification'))},
        ),
    ]
