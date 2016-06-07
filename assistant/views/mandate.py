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
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import csv, codecs
from assistant.forms import MandateForm
from base.views import layout
from assistant.models import assistant_mandate, academic_assistant, mandate_structure
from base import models as mdl
from base.views.layout import render_to_response
from django.http.response import HttpResponseRedirect
from base.views.common import academic_year



@login_required
def mandate_edit(request, mandate_id):
    mandate = assistant_mandate.find_mandate_by_id(mandate_id)
    form = MandateForm(initial={'comment': mandate.comment, 
                                'renewal_type': mandate.renewal_type,
                                'absences': mandate.absences,
                                'other_status': mandate.other_status,
                                'contract_duration': mandate.contract_duration,
                                'contract_duration_fte': mandate.contract_duration_fte
                                })
    return layout.render(request, 'mandate_form.html', {'mandate': mandate,
                                                'form': form})


def mandate_save(request, mandate_id):
    form = MandateForm(data=request.POST)
    mandate = assistant_mandate.find_mandate_by_id(mandate_id)
    # get the screen modifications
    if request.POST['comment']:
        mandate.comment = request.POST['comment']
        mandate.absences = request.POST['absences']
    else:
        mandate.comment = None
        mandate.absences = None
    if request.POST['absences']:
        mandate.absences = request.POST['absences']
    else:
        mandate.absences = None
    if request.POST['other_status']:
        mandate.other_status = request.POST['other_status']
    else:
        mandate.other_status = None
    mandate.renewal_type = request.POST['renewal_type']
    if form.is_valid():
        mandate.save()
        return mandate_edit(request, mandate.id)
    else:
        return layout.render(request, "mandate_form.html", {'mandate': mandate,
                                                                 'form': form})    



def load_mandates(request):
    """Importe un fichier CSV osis/assistant/views/data_assistant.csv contenant la liste des mandats.
    Si un mandat avec un assistant, sap_id, position_id et academic_year existe déjà,
    il est mis à jour plutôt qu'ajouté.
    Si l'assistant lié au mandat existe déjà, il n'est ni modifié ni ajouté"""
    
    imported_assistants_counter = 0
    imported_mandates_counter = 0
    updated_mandates_counter = 0
    error_counter = 0
    if(request.POST):
        with codecs.open('osis/assistant/views/data_assistant.csv', encoding='utf-8') as csvfile:
            row = csv.reader(csvfile, delimiter=';')
            for columns in row:
                if len(columns) > 0:
                    person = mdl.person.find_by_global_id(columns[5].strip())
                    if person:
                        assistant = academic_assistant.AcademicAssistant()
                        assistant.person = person
                        fte = columns[8].strip().replace(",", ".");
                        this_academic_year = mdl.academic_year.current_academic_year()
                        position_id = columns[3].strip()
                        faculty = columns[1].strip()
                        institute = columns[2].strip()
                        sap_id = columns[4].strip()  
                        entry_date = columns[10].strip()
                        end_date = columns[10].strip()
                        contract_duration = columns[14].strip()
                        contract_duration_fte = columns[15].strip()
                        renewal_type = columns[16].strip()
                        assistant_type = columns[11].strip()
                        grade = columns[12].strip()
                        scale = columns[13].strip()
                        renewal_type = columns[16].strip()
                        absences =columns[17].strip()
                        comment =columns[18].strip()
                        other_status = columns[19].strip()
                        mandate = assistant_mandate.AssistantMandate()
                        mandate.fulltime_equivalent = fte
                        mandate.position_id = position_id
                        mandate.sap_id = sap_id 
                        mandate.entry_date = entry_date
                        mandate.end_date = end_date
                        mandate.assistant_type = assistant_type
                        mandate.grade = grade
                        mandate.scale = scale
                        mandate.contract_duration = contract_duration
                        mandate.contract_duration_fte = contract_duration_fte
                        mandate.renewal_type = renewal_type
                        mandate.absences = absences
                        mandate.comment = comment
                        mandate.other_status = other_status
                        mandate.state='TO_DO'
                        mandate.research_percent=0
                        mandate.tutoring_percent=0
                        mandate.service_activities_percent=0
                        mandate.formation_activities_percent=0
                        mandate.faculty_representation=0
                        mandate.institute_representation=0
                        mandate.sector_representation=0
                        mandate.governing_body_representation=0
                        mandate.corsci_representation=0
                        mandate.students_service=0
                        mandate.infrastructure_mgmt_service=0
                        mandate.events_organisation_service=0
                        mandate.publishing_field_service=0
                        mandate.scientific_jury_service=0
                        mandate.academic_year=this_academic_year
                        mandate.appeal='NONE'
                        mandate.special=False
                        try:
                            assistant.save()
                            imported_assistants_counter += 1
                        except IntegrityError:
                            print('Duplicated : %s - %s' % (assistant, person))
                        try:
                            mandate.assistant=academic_assistant.find_by_person(person)
                            existing_mandate = assistant_mandate.AssistantMandate.objects.filter(academic_year = this_academic_year,
                                                                                                 assistant = mandate.assistant,
                                                                                                 sap_id = sap_id,
                                                                                                 position_id = position_id)
                            if existing_mandate.count() >0:
                                existing_mandate.update(fulltime_equivalent=fte,
                                               entry_date = entry_date,
                                               end_date = end_date,
                                               contract_duration = contract_duration,
                                               contract_duration_fte = contract_duration_fte,
                                               renewal_type = renewal_type,
                                               assistant_type = assistant_type,
                                               grade = grade,
                                               scale = scale,
                                               absences = absences,
                                               comment = comment,
                                               other_status = other_status)
                                updated_mandates_counter += 1
                            else:
                                mandate.save()
                                if institute:
                                    existing_institute = mdl.structure.Structure.objects.get(acronym=institute,
                                                                                         type='INSTITUTE')
                                    if existing_institute:
                                        mandate_struc_institute = mandate_structure.MandateStructure()
                                        mandate_struc_institute.assistant_mandate = mandate
                                        mandate_struc_institute.structure = existing_institute
                                        mandate_struc_institute.save()
                                if faculty:
                                    existing_faculty = mdl.structure.Structure.objects.get(acronym=faculty,
                                                                                       type='FACULTY')
                                    if existing_faculty:
                                        mandate_struc_faculty = mandate_structure.MandateStructure()
                                        mandate_struc_faculty.assistant_mandate = mandate
                                        mandate_struc_faculty.structure = existing_faculty
                                        mandate_struc_faculty.save()
                                imported_mandates_counter += 1
                        except IntegrityError:
                            print('Duplicated : %s' % (assistant))
                    else:
                        error_counter += 1
    return layout.render(request, "load_mandates.html", {'imported_assistants': imported_assistants_counter,
                                                         'imported_mandates': imported_mandates_counter,
                                                         'updated_mandates': updated_mandates_counter,
                                                         'error_counter': error_counter})             
 


