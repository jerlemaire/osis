##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2016 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
import logging
from django.conf import settings
from django.db import models
from django.core import serializers
import uuid
from pika.exceptions import ChannelClosed, ConnectionClosed
from backoffice.queue import queue_actions

QUEUE_NAME = "osis_portal"
LOGGER = logging.getLogger(settings.DEFAULT_LOGGER)


class SerializableModelManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class SerializableModel(models.Model):
    objects = SerializableModelManager()

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    def save(self, *args, **kwargs):
        super(SerializableModel, self).save(*args, **kwargs)
        try:
            queue_actions.send_message(QUEUE_NAME, serialize_objects([self]))
        except (ChannelClosed, ConnectionClosed) :
            LOGGER.warning('QueueServer is not installed or not launched')

    def natural_key(self):
        return [self.uuid]

    def __str__(self):
        return self.uuid

    class Meta:
        abstract = True


def serialize_objects(objects, format='json'):
    """
    Serialize all objects given by parameter.
    All objects must come from the same model. Otherwise, an exception will be thrown.
    If the object contains a FK 'user', this field will be ignored for the serialization.
    :param objects: List of objects to serialize.
    :return: Json data containing serializable objects.
    """
    if not objects:
        return None
    if len([obj.__class__ for obj in objects]) > 1:
        raise Exception("Please give objects for only 1 model at the same time")
    model_class = objects[0].__class__
    return serializers.serialize(format,
                                 objects,
                                 # indent=2,
                                 fields=[field.name for field in model_class._meta.fields if field.name != 'user'],
                                 use_natural_foreign_keys=True,
                                 use_natural_primary_keys=True)