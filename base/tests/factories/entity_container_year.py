##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
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
import datetime
import operator

import factory
import factory.fuzzy
from django.conf import settings
from django.utils import timezone

from base.models.enums import entity_container_year_link_type
from base.tests.factories.entity import EntityFactory
from base.tests.factories.learning_container_year import LearningContainerYearFactory


def _get_tzinfo():
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class EntityContainerYearFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "base.EntityContainerYear"

    external_id = factory.Sequence(lambda n: '10000000%02d' % n)
    changed = factory.fuzzy.FuzzyDateTime(datetime.datetime(2016, 1, 1, tzinfo=_get_tzinfo()),
                                          datetime.datetime(2017, 3, 1, tzinfo=_get_tzinfo()))
    entity = factory.SubFactory(EntityFactory)
    learning_container_year = factory.SubFactory(LearningContainerYearFactory)
    type = factory.Iterator(entity_container_year_link_type.ENTITY_CONTAINER_YEAR_LINK_TYPES,
                            getter=operator.itemgetter(0))