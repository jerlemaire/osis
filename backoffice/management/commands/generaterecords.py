from pickle import load

from django.core.management.base import BaseCommand, CommandError

from base.models import offer
from base.models.person import Person
from django.contrib.auth.models import User
from base import models as mdl_base
from reference import models as mdl_reference
from attribution import models as mdl_attribution
from faker import Faker
from backoffice.management.commands import generate_records_academic_year
from backoffice.management.commands import generate_records_academic_calendar
from backoffice.management.commands import generate_records_offer
from backoffice.management.commands import  generate_records_offer_year_calendar
from backoffice.management.commands import generate_records_offer_year

import datetime


fake = Faker()


def create_record(model_class, **kwargs):
    model_class.objects.create(**kwargs)



def create_be_country():
    country = mdl_reference.country.Country.objects.create( name='Belgique',iso_code='BE',nationality='Belge',cref_code='04')

    return country


def create_organization():
    organisation = mdl_base.organization.Organization.objects.create(name='Université catholique de Louvain',
                                                                     acronym='UCL', reference='-',
                                                                     website='http://uclouvain.be', type='Main')
    return organisation

def create_organization_adress(organisation,localisation,cp,city,country ):
    organisation_adres = mdl_base.organization_address.OrganizationAddress.objects.create(organization=organisation,
                                                                                          label='-',
                                                                                          location=localisation,
                                                                                          postal_code=cp,
                                                                                          city=city,country=country)
    return organisation_adres



def create_sector(acronym,title,organisation,type):
    structure_sector = mdl_base.structure.Structure.objects.create(acronym=acronym,
                                                                   title=title, organization=organisation, type=type)
    return structure_sector

def create_structure(acronym,titre,structure_part_of,organisation,type):
    structure = mdl_base.structure.Structure.objects.create(acronym=acronym, title=titre,
                                                                part_of=structure_part_of, organization=organisation,
                                                                type=type)
    return structure


def create_campus(name,organisation):
    campus = mdl_base.campus.Campus.objects.create(name=name, organization=organisation)
    return campus


def create_learning_unit(acronym,title,start_year, end_year):
    learning_unit = mdl_base.learning_unit.LearningUnit.objects.create(acronym=acronym,title=title,start_year=start_year,end_year=end_year)
    return learning_unit

def create_learning_unit_year(academic_year,learning_unit,acronym,title,credits):
    decimal_scores=False
    if (credits >=15):
        decimal_scores =True
    learning_unit_year = mdl_base.learning_unit_year.LearningUnitYear.objects.create(
        academic_year=academic_year, learning_unit=learning_unit,
        acronym=acronym, title=title, credits=credits, decimal_scores=decimal_scores)
    return learning_unit_year


def create_user(username, password, email):
    an_username =username
    while(check_user_id_exist(username)==True):
        an_username=fake.user_name()
    user = User.objects.create(username=an_username, password=password, email=email)
    return user

def check_user_id_exist(a_username):
    users = User.objects.filter(username=a_username)
    if(users==None or len(users) == 0):
        return False
    return True



def create_person(user):
    person = Person.objects.create(user=user, first_name=fake.first_name(),
                                               last_name=fake.last_name())
    return person

def create_program_manager(person,offer_year):
    program_manager = mdl_base.program_manager.ProgramManager.objects.create(person=person,offer_year=offer_year)
    return program_manager

def create_tutor(person):
    tutor = mdl_base.tutor.Tutor.objects.create(person=person)
    return tutor

def create_attribution(learning_unit_year,tutor, score_responsible):
    attribution = mdl_attribution.attribution.Attribution.objects.create(learning_unit_year = learning_unit_year,tutor=tutor, score_responsible= score_responsible)
    return attribution

def create_student(user):
    person = create_person(user)
    student = mdl_base.student.Student.objects.create(person=person, registration_id=fake.ean(length=8))
    return student

def create_offer_enrollement(student,offer_year):
    offer_enrollment = mdl_base.offer_enrollment.OfferEnrollment.objects.create(student=student,offer_year=offer_year, date_enrollment =datetime.date.today())
    return offer_enrollment

def create_learning_unit_enrollement(learning_unit_year,offer_enrollment):
    learning_unit_enrollement = mdl_base.learning_unit_enrollment.LearningUnitEnrollment.objects.create(learning_unit_year=learning_unit_year,offer_enrollment=offer_enrollment ,
                                                                                                        date_enrollment =datetime.date.today())
    return learning_unit_enrollement

def create_session_exam(number_session, learning_unit_year, offer_year_calendar):
    session_exam = mdl_base.session_exam.SessionExam.objects.create(number_session=number_session,
                                              learning_unit_year=learning_unit_year,
                                              offer_year_calendar=offer_year_calendar)
    return session_exam


def create_exam_enrollment(session_exam, learning_unit_enrollment):
        an_exam_enrollment = mdl_base.exam_enrollment.ExamEnrollment.objects.create(session_exam=session_exam,
                                                            learning_unit_enrollment=learning_unit_enrollment)
        return an_exam_enrollment


def make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year,student,offer_year,session_exam):
    learning_unit_enrollment = create_learning_unit_enrollement(learning_unit_year,
                                                                create_offer_enrollement(student, offer_year))
    sess_exam_enrollment = create_exam_enrollment(session_exam, learning_unit_enrollment)





class Command(BaseCommand):
    #Creates the records for the database

    def handle(self, *args, **options):
        tel_sc = '010473324'
        fax_sc = '010472837'
        recipient_sc = 'SC'
        adres_sc = 'Place des Sciences, 2L6.06.01'
        localisation_lln = 'Louvain-la-Neuve'
        cp_lln = 1348
        city = 'Ottignies'
        acronym_chim_learning = 'LCHM1111'
        acronym_biol_learning = 'LENVI2199'
        title_chim_learning = 'Chimie générale 1'
        title_biol_learning = 'Stage professionnel'
        end_learning = 2099
        bac_sc='Bachelier en sciences'
        acr_ch='CHIM'
        acr_biol = 'BIOL'
        acr_sc = 'SC'
        country = create_be_country()
        organisation = create_organization()
        organisation_adres = create_organization_adress(organisation, localisation_lln, cp_lln, city, country)
        structure_sector = create_sector('SST', 'Secteur des sciences et technologies', organisation, 'SECTOR')
        structure_fac = create_structure(acr_sc, 'Faculté des sciences', structure_sector, organisation, 'FACULTY')
        structure_pgm_chim = create_structure(acr_ch, 'Ecole de chimie', structure_fac, organisation,
                                              'PROGRAM_COMMISION')
        structure_pgm_biol = create_structure(acr_biol, 'Ecole de biologie', structure_fac, organisation,
                                              'PROGRAM_COMMISION')
        campus = create_campus(localisation_lln, organisation)

        academic_year = generate_records_academic_year.create_academic_year_actual()
        academic_calendar_score_encoding_sess_in = generate_records_academic_calendar.create_academic_calendar_encoding_event_in(
            academic_year)

        academic_calendar_score_delibe_sess_in = generate_records_academic_calendar.create_academic_calendar_delibe_event_in(
            academic_year)

        offer =  generate_records_offer.create_offer(bac_sc)
        offer_year_chim =generate_records_offer_year.create_offer_year(offer,academic_year,structure_sector,structure_fac,structure_fac,'CHIM11BA','Première année de bachelier en sciences chimiques',
                                      'I Ba en scs chimiques','Bachelier',recipient_sc,adres_sc,cp_lln,localisation_lln,country,campus)

        offer_year_calendar_chim_score_encoding_sess_past = generate_records_offer_year_calendar.create_offer_year_calendar_in_past(offer_year_chim, academic_calendar_score_encoding_sess_in)
        offer_year_calendar_chim_score_encoding_sess_fiture = generate_records_offer_year_calendar.create_offer_year_calendar_in_fiture (
            offer_year_chim, academic_calendar_score_encoding_sess_in)
        offer_year_calendar_chim_score_encoding_sess_in = generate_records_offer_year_calendar.create_offer_year_calendar(offer_year_chim, academic_calendar_score_encoding_sess_in,None,None)


        offer_year_calendar_chim_score_delibe_sess_past = generate_records_offer_year_calendar.create_offer_year_calendar_in_past(
            offer_year_chim, academic_calendar_score_encoding_sess_in)
        offer_year_calendar_chim_score_delibe_sess_fiture = generate_records_offer_year_calendar.create_offer_year_calendar_in_fiture(
            offer_year_chim, academic_calendar_score_encoding_sess_in)
        offer_year_calendar_chim_score_delibe_sess_in = generate_records_offer_year_calendar.create_offer_year_calendar(
            offer_year_chim, academic_calendar_score_encoding_sess_in, None, None)


        credits = 10

        #decimal score not allowed
        learning_unit_chim = create_learning_unit(acronym_chim_learning,title_chim_learning,2004,end_learning)
        learning_unit_year_chim = create_learning_unit_year(academic_year,
                                                                               learning_unit_chim,
                                                                               acronym_chim_learning, title_chim_learning,
                                                                               credits)
        credits = 20
        #decimal score allowed
        learning_unit_biol =  create_learning_unit(acronym_biol_learning,title_biol_learning,2007,end_learning)
        learning_unit_year_biol = create_learning_unit_year(academic_year,learning_unit_biol,acronym_biol_learning,title_biol_learning,credits)


        #program manager
        user_pgm_manager = create_user('eni','evase','evase@gmail.com')
        person_pgm_manager = create_person(user_pgm_manager)
        program_manager_chim =create_program_manager(person_pgm_manager,offer_year_chim)
        #program_manager_biol = create_program_manager(person_pgm_manager, offer_year_biol)

        #prof leader
        user_chim_learning_unit_tutor_leader =create_user('eniLchim','evaseLchim','evaseChim@gmail.com')
        person_chim_learning_unit_tutor_leader =create_person(user_chim_learning_unit_tutor_leader)
        tutor_chim_learning_unit = create_tutor(person_chim_learning_unit_tutor_leader) #tutor and leader of lchm1111
        create_attribution(learning_unit_year_chim,tutor_chim_learning_unit,True)


        user_biol_learning_unit_tutor_leader = create_user('eniLbiol', 'evaseLbiol', 'evaseBiol@gmail.com')
        person_biol_learning_unit_tutor_leader = create_person(user_biol_learning_unit_tutor_leader)
        tutor_biol_learning_unit = create_tutor(person_biol_learning_unit_tutor_leader)  # tutor and leader of LENVI2199
        create_attribution(learning_unit_year_biol, tutor_biol_learning_unit,False)
        #prof
        user_chim_learning_unit_tutor= create_user('eniTchim', 'evaseTchim', 'evase@gmail.com')
        person_chim_learning_unit_tutor = create_person(user_chim_learning_unit_tutor)
        tutor2_chim_learning_unit = create_tutor(person_chim_learning_unit_tutor)  # tutor  of lchm1111
        create_attribution(learning_unit_year_chim, tutor2_chim_learning_unit,True)


        user_biol_learning_unit_tutor = create_user('eniTbiol', 'evaseTbiol', 'evase@gmail.com')
        person_biol_learning_unit_tutor = create_person( user_biol_learning_unit_tutor)
        tutor2_biol_learning_unit = create_tutor(person_biol_learning_unit_tutor)  # tutor  of LENVI2199
        create_attribution(learning_unit_year_biol, tutor2_biol_learning_unit,False)
        
        #session_exam of courses
        #session_exam_1_learning_unit_chim = create_session_exam(1, learning_unit_year_chim, offer_year_calendar_chim_score_encoding_sess_1)
        #session_exam_2_learning_unit_chim = create_session_exam(2, learning_unit_year_chim, offer_year_calendar_chim_score_encoding_sess_2)
        #session_exam_3_learning_unit_chim = create_session_exam(3, learning_unit_year_chim, offer_year_calendar_chim_score_encoding_sess_3)

        # session_exam of courses
        #session_exam_1_learning_unit_biol = create_session_exam(1, learning_unit_year_biol, offer_year_calendar_biol_score_encoding_sess_1)
        #session_exam_2_learning_unit_biol = create_session_exam(2, learning_unit_year_biol, offer_year_calendar_biol_score_encoding_sess_2)
        #session_exam_3_learning_unit_biol = create_session_exam(3, learning_unit_year_biol, offer_year_calendar_biol_score_encoding_sess_3)


        #student  and offer enrollment and  learning unity

        for i in range(0, 50):
            user = create_user(fake.user_name(),fake.password(),fake.email())
            student =create_student(user)
            #if(i%2==0):
            #   make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year_chim, student, offer_year_chim, session_exam_1_learning_unit_chim)

            #else :
            #   make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year_biol, student, offer_year_biol, session_exam_1_learning_unit_biol)

        for i in range(0, 60):
                user = create_user(fake.user_name(), fake.password(), fake.email())
                student = create_student(user)
                #if (i % 2 == 0):
                #   make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year_chim, student, offer_year_chim, session_exam_2_learning_unit_chim)
                    #else:
                    #   make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year_biol, student, offer_year_biol, session_exam_2_learning_unit_biol)
        for i in range(0, 70):
            user = create_user(fake.user_name(),fake.password(),fake.email())
            student =create_student(user)
            #if(i%2==0):
            #    make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year_chim, student, offer_year_chim, session_exam_3_learning_unit_chim)
                #else:
                # make_learning_unit_enrolement_and_exam_enrollment(learning_unit_year_biol, student, offer_year_biol, session_exam_3_learning_unit_biol)

