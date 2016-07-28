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
from django.contrib import admin


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'decree')
    fieldsets = ((None, {'fields': ('name', 'parent', 'decree')}),)


class Domain(models.Model):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True)
    decree = models.ForeignKey('Decree')

    def __str__(self):
        return self.name


def find_all_for_sync():
    """
    :return: All records in the 'Domain' model (table). Used to synchronize date from Osis to Osis-portal.
    """
    print("Retrieving data from " + str(Domain) + "...")
    # Necessary fields for Osis-portal
    fields = ['id', 'external_id', 'name', 'parent_id']
    # list() to force the evaluation of the queryset
    return list(Domain.objects.values(*fields).order_by('name'))