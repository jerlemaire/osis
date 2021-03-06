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
from django.db import models


# To be removed.
class Attribution(models.Model):
    FUNCTION_CHOICES = (
        ('COORDINATOR', 'Coordinator'),
        ('PROFESSOR', 'Professor'))

    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed = models.DateTimeField(null=True, auto_now=True)
    start_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    function = models.CharField(max_length=15, blank=True, null=True, choices=FUNCTION_CHOICES, db_index=True)
    learning_unit_year = models.ForeignKey('LearningUnitYear', related_name='learning_unit_year_attribution', blank=True, null=True, default=None)
    tutor = models.ForeignKey('Tutor', related_name='tutor_attribution')

    def __str__(self):
        return u"%s - %s" % (self.tutor.person, self.function)
