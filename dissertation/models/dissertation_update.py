##############################################################################
#
# OSIS stands for Open Student Information System. It's an application
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
from django.db import models
from . import dissertation


class DissertationUpdate(models.Model):

    status_from = models.CharField(max_length=12, choices=dissertation.STATUS_CHOICES, default='DRAFT')
    status_to = models.CharField(max_length=12, choices=dissertation.STATUS_CHOICES, default='DRAFT')
    created = models.DateTimeField(auto_now_add=True)
    justification = models.TextField(default=' ')
    person = models.ForeignKey('base.Person')
    dissertation = models.ForeignKey(dissertation.Dissertation)

    def __str__(self):
        desc = self.dissertation.title + ' / ' + self.status_from + ' >> ' + self.status_to \
               + ' / ' + str(self.created)

        return desc