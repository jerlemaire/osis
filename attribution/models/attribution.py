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
from django.db import models
from attribution.models.enums import function
from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin


class AttributionAdmin(SerializableModelAdmin):
    list_display = ('tutor', 'function', 'score_responsible', 'learning_unit_year', 'start_year', 'end_year', 'changed')
    list_filter = ('function', 'learning_unit_year__academic_year')
    fieldsets = ((None, {'fields': ('learning_unit_year', 'tutor', 'function', 'score_responsible', 'start_year',
                                    'end_year')}),)
    raw_id_fields = ('learning_unit_year', 'tutor')
    search_fields = ['tutor__person__first_name', 'tutor__person__last_name', 'learning_unit_year__acronym',
                     'tutor__person__global_id']


class Attribution(SerializableModel):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    changed = models.DateTimeField(null=True)
    start_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    end_date = models.DateField(auto_now=False, blank=True, null=True, auto_now_add=False)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    function = models.CharField(max_length=35, blank=True, null=True, choices=function.FUNCTIONS, db_index=True)
    learning_unit_year = models.ForeignKey('base.LearningUnitYear', blank=True, null=True, default=None)
    tutor = models.ForeignKey('base.Tutor')
    score_responsible = models.BooleanField(default=False)

    def __str__(self):
        return u"%s - %s" % (self.tutor.person, self.function)


def search(tutor=None, learning_unit_year=None, score_responsible=None, list_learning_unit_year=None):
    queryset = Attribution.objects

    if tutor:
        queryset = queryset.filter(tutor=tutor)

    if learning_unit_year:
        queryset = queryset.filter(learning_unit_year=learning_unit_year)

    if score_responsible is not None:
        queryset = queryset.filter(score_responsible=score_responsible)

    if list_learning_unit_year:
        queryset = queryset.filter(learning_unit_year__in=list_learning_unit_year)

    return queryset.select_related('tutor', 'learning_unit_year')


def find_all_responsibles(a_learning_unit_year):
    attribution_list = Attribution.objects.select_related("tutor") \
        .filter(learning_unit_year=a_learning_unit_year) \
        .filter(score_responsible=True)
    return [attribution.tutor for attribution in attribution_list]


def find_responsible(a_learning_unit_year):
    tutors_list = find_all_responsibles(a_learning_unit_year)
    if tutors_list:
        return tutors_list[0]
    return None


def is_score_responsible(user, learning_unit_year):
    attributions = Attribution.objects.filter(learning_unit_year=learning_unit_year) \
        .filter(score_responsible=True) \
        .filter(tutor__person__user=user) \
        .count()
    return attributions > 0
