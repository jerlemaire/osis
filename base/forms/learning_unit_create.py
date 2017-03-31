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
from django import forms
from base import models as mdl
from django.utils import timezone
from django.core.exceptions import ValidationError
from base.enums import learning_unit_year_types


class LearningUnitCreateForm(forms.Form):

    academic_year=forms.CharField(widget=forms.TextInput(attrs={'size':'10'}),max_length=4, required=True)
    academic_year_id=forms.CharField(widget=forms.HiddenInput())
    acronym = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}),max_length=20, required=True)
    type = forms.CharField(
        widget=forms.Select(choices=learning_unit_year_types.LEARNING_UNIT_YEAR_TYPES),
        required=True
    )
    type_complement = forms.CharField(
        widget=forms.Select(choices=learning_unit_year_types.LEARNING_UNIT_YEAR_TYPES_COMPLEMENT),
        required=True
    )

    def clean(self):
        clean_data=self.cleaned_data
        if (not clean_data):
            raise ValidationError('INVALID')
        return clean_data


def get_academic_year_relative(academic_year):
    year = timezone.now().year
    month = timezone.now().month
    if (month>=9 and month<=12):
        academic_year_relative=academic_year
    elif (month>=1 and month<=8 and academic_year==year):
        academic_year_relative=academic_year
    elif (month>=1 and month<=8 and academic_year<year):
        academic_year_relative=academic_year+1
    else:
        academic_year_relative=academic_year
    return academic_year_relative


def check_learning_units_with_acronym(acronym):
    learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
    if not learning_units:
        raise ValidationError('ACADEMIC_YEAR_WITH_ACRONYM')


def get_learning_units_with_acronym(acronym):
    learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
    if not learning_units:
        learning_unit_create=True
    else:
        learning_unit_create=False
    return learning_unit_create
