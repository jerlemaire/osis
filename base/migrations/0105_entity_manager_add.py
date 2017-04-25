# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from base.models.entity_manager import EntityManager
from base.models.structure import Structure
from base.models.person import Person

data_to_import = {
    'AGRO': '00003962',
    'DRT': '00029932',
    'EPL': '00033087',
    'ESPO': '00032935',
    'FASB': '00035177',
    'FIAL': '00187386',
    'FSM': '00034519',
    'FSP': '00035177',
    'LOCI': '00086669',
    'LSM': '00030570',
    'MEDE': '00035177',
    'PSP': '00052832',
    'SC': '00227397',
    'TECO': '00095684',
}


def add_entity_managers(apps, schema_editor):
    for entity_acronym, global_id in data_to_import.items():
        a_person = Person.objects.filter(person__global_id=global_id)
        entity = Structure.objects.filter(acronym=entity_acronym)
        if a_person and entity:
            if not _entity_manager_exists(a_person, _entity):
                new_entity_manager = EntityManager(person=a_person,
                                                   structure=entity)
                new_entity_manager.save()


def _entity_manager_exists(a_person, a_structure):
    return EntityManager.objects.filter(person=a_person) \
        .filter(structure=a_structure) \
        .exists()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0104_'),
    ]

    operations = [
        migrations.RunPython(add_entity_managers),
    ]
