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

from django.utils.translation import ugettext_lazy as _

#Errors handling on form
lu_error_required = 'This field is required'
lu_error_invalid = 'Enter a valid value'
lu_error_academic_year_required = 'Please specify an academic year'
lu_error_academic_year_with_acronym = 'Please specify an academic year or enter a valid acronym.'
lu_error_invalid_search = 'Invalid search - Please fill some information before executing a search.'
#Periodicity types
lu_period_annual = "Annual"
lu_period_biennal_even = "Biennal even"
lu_period_biennal_odd = "Bennial odd"
#Status in model learning_unit_year
luy_status_none = ""
luy_status_valid = "Valid"
luy_status_invalid = "Invalid"
#Types in model learning_unit_year
luy_type_none = ""
luy_type_course = "Course"
luy_type_master_thesis = "Master thesis"
luy_type_internship = "Internship"
luy_type_course_with_pc = "Course with practical classes"

LEARNING_UNIT_ERRORS = (
    (lu_error_required, _('This field is required')),
    (lu_error_invalid, _('Enter a valid value')),
    (lu_error_academic_year_required, _('Please specify an academic year')),
    (lu_error_invalid_search, _('Invalid search - Please fill some information before executing a search.')),
    (lu_error_academic_year_with_acronym, _('Please specify an academic year or enter a valid acronym.'))
)

LEARNING_UNIT_PERIODICITY_TYPES = (
    (lu_period_annual,  _('ANNUAL')),
    (lu_period_biennal_even,  _('BIENNIAL_EVEN')),
    (lu_period_biennal_odd,  _('BIENNIAL_ODD')))

LEARNING_UNIT_YEAR_STATUS = (
    (luy_status_none, _('None')),
    (luy_status_valid, _('Valid')),
    (luy_status_invalid, _('Invalid'))
)

LEARNING_UNIT_YEAR_TYPES = (
    (luy_type_none, _('None')),
    (luy_type_course, _('Course')),
    (luy_type_master_thesis, _('Master thesis')),
    (luy_type_internship, _('Internship')),
    (luy_type_course_with_pc, _('Course with practical classes'))
)