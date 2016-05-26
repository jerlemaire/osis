# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-26 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0032_auto_20160526_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dissertation',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Draft'), ('DIR_SUBMIT', 'Submitted to Director'), ('DIR_OK', 'Accepted by Director'), ('DIR_KO', 'Refused by Director'), ('COM_SUBMIT', 'Submitted to Commission'), ('COM_OK', 'Accepted by Commission'), ('COM_KO', 'Refused by Commission'), ('EVA_SUBMIT', 'Submitted to First Year Evaluation'), ('EVA_OK', 'Accepted by First Year Evaluation'), ('EVA_KO', 'Refused by First Year Evaluation'), ('TO_RECEIVE', 'To be received'), ('TO_DEFEND', 'To be defended'), ('DEFENDED', 'Defended'), ('ENDED', 'Ended'), ('ENDED_WIN', 'Ended Win'), ('ENDED_LOS', 'Ended Los')], default='DRAFT', max_length=12),
        ),
    ]
