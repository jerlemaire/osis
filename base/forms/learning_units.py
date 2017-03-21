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
from base.enums import learning_unit_year_status
from base.enums import learning_unit_year_types
from base.enums import learning_units_errors

class LearningUnitsForm(forms.Form):

    academic_year=forms.CharField(max_length=10, required=False)
    acronym = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}),max_length=20, required=False)
    keyword = forms.CharField(widget=forms.TextInput(attrs={'size':'10'}),max_length=20, required=False)
    type = forms.CharField(
        widget=forms.Select(choices=learning_unit_year_types.LEARNING_UNIT_YEAR_TYPES),
        required=False
    )
    status=forms.CharField(
        widget=forms.Select(choices=learning_unit_year_status.LEARNING_UNIT_YEAR_STATUS),
        required=False
    )

    def clean(self):
        clean_data=self.cleaned_data
        academic_year = clean_data.get('academic_year')
        acronym = clean_data.get('acronym').upper()
        keyword = clean_data.get('keyword')
        status = clean_data.get('status')
        type = clean_data.get('type')

        if (not acronym and not keyword and status=="NONE" and type=="NONE"):
            raise ValidationError(learning_units_errors.INVALID_SEARCH)
        elif academic_year=="0":
            check_when_academic_year_is_all(acronym)
        return clean_data

    def set_academic_years_all(self):
        academic_year = self.cleaned_data.get('academic_year')
        if academic_year=="0":
            academic_years_all=1
        else:
            academic_years_all=0
        return academic_years_all

    def get_learning_units(self):
        academic_year = self.cleaned_data.get('academic_year')
        acronym = self.cleaned_data.get('acronym').upper()
        keyword = self.cleaned_data.get('keyword')
        status = self.cleaned_data.get('status')
        type = self.cleaned_data.get('type')
        if status=="NONE":
            status=None
        if type=="NONE":
            type=None
        if (academic_year=="0" and acronym and not keyword and not status and not type):
            learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
        else:
            if (academic_year=="0"):
                learning_units = mdl.learning_unit_year.search(academic_year_id=None,acronym=acronym,title=keyword,type=type,status=status)
            else:
                learning_units = mdl.learning_unit_year.search(academic_year_id=academic_year,acronym=acronym,title=keyword,type=type,status=status)
        return learning_units

    def get_academic_year(self):
        academic_year = self.cleaned_data.get('academic_year')
        return academic_year

    def check_learning_unit_create(self):
        clean_data=self.cleaned_data
        academic_year = clean_data.get('academic_year')
        acronym = clean_data.get('acronym').upper()
        keyword = clean_data.get('keyword')
        status = clean_data.get('status')
        type = clean_data.get('type')
        if not academic_year or not acronym:
            learning_unit_create=False
        else:
            academic_year=mdl.academic_year.find_academic_year_by_id(int(academic_year)).year
            academic_year_relative = get_academic_year_relative(int(academic_year))
            if academic_year_relative>=timezone.now().year and not keyword and status=="NONE" and type=="NONE":
                learning_unit_create=get_learning_units_with_acronym(acronym)
            else:
                learning_unit_create=False
        return learning_unit_create

    def set_request_session(self,request):
        acronym=self.cleaned_data.get('acronym')
        academic_year_id=self.cleaned_data.get('academic_year')
        academic_year=mdl.academic_year.find_academic_year_by_id(int(academic_year_id)).__str__()
        request.session['academic_year'] = academic_year
        request.session['acronym'] = acronym
        return request.session


def check_when_academic_year_is_all(acronym):
    if (acronym):
        check_learning_units_with_acronym(acronym)
    elif (not acronym):
        raise ValidationError(learning_units_errors.ACADEMIC_YEAR_REQUIRED)


def check_learning_units_with_acronym(acronym):
    learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
    if not learning_units:
        raise ValidationError(learning_units_errors.ACADEMIC_YEAR_WITH_ACRONYM)


def get_learning_units_with_acronym(acronym):
    learning_units=mdl.learning_unit_year.find_by_acronym(acronym)
    if not learning_units:
        learning_unit_create=True
    else:
        learning_unit_create=False
    return learning_unit_create


def get_academic_year_relative(academic_year):
    year = timezone.now().year
    month = timezone.now().month
    if month>=9 and month<=12:
        academic_year_relative=academic_year
    elif month>=1 and month<=8 and academic_year==year:
        academic_year_relative=academic_year
    elif month>=1 and month<=8 and academic_year<year:
        academic_year_relative=academic_year+1
    else:
        academic_year_relative=academic_year
    return academic_year_relative
