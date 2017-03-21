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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory

from base.tests.models import test_exam_enrollment, test_offer_year_calendar, test_offer_enrollment,\
    test_learning_unit_enrollment, test_session_exam
from attribution.tests.models import test_attribution
from assessments.views import score_encoding
from base.models.exam_enrollment import ExamEnrollment

from base.tests.factories.academic_year import AcademicYearFactory
from base.tests.factories.program_manager import ProgramManagerFactory
from base.tests.factories.learning_unit_year import LearningUnitYearFactory
from base.tests.factories.tutor import TutorFactory
from base.tests.factories.person import PersonFactory
from base.tests.factories.offer_year import OfferYearFactory
from base.tests.factories.student import StudentFactory
from django.utils import timezone


class OnlineEncodingTest(TestCase):
    def setUp(self):
        academic_year = AcademicYearFactory(year=datetime.now().year)
        self.learning_unit_year = LearningUnitYearFactory(acronym="LMEM2110",
                                                          title="Recent Continental Philosophy",
                                                          academic_year=academic_year)
        self.offer_year_1 = OfferYearFactory(acronym="SINF2MA", title="Master en Sciences Informatique",
                                             academic_year=academic_year)
        self.offer_year_2 = OfferYearFactory(acronym="DROI1BA", title="Bachelier en droit",
                                             academic_year=academic_year)
        self.exam_enrollment_1 = test_exam_enrollment.create_exam_enrollment_with_student(1, "64641200", self.offer_year_1, self.learning_unit_year,
                                                                     academic_year)
        self.exam_enrollment_2 = test_exam_enrollment.create_exam_enrollment_with_student(2, "60601200", self.offer_year_2, self.learning_unit_year,
                                                                     academic_year)

        self.tutor = TutorFactory()
        test_attribution.create_attribution(tutor=self.tutor, learning_unit_year=self.learning_unit_year)
        add_permission(self.tutor.person.user, "can_access_scoreencoding")

        self.program_manager_1 = ProgramManagerFactory(offer_year=self.offer_year_1)
        add_permission(self.program_manager_1.person.user, "can_access_scoreencoding")

        self.program_manager_2 = ProgramManagerFactory(offer_year=self.offer_year_2)
        add_permission(self.program_manager_2.person.user, "can_access_scoreencoding")

        self.Client = Client()

    def test_filter_enrollments_by_offer_year(self):
        enrollments = [self.exam_enrollment_1, self.exam_enrollment_2]

    def test_get_special_closing_date_for_tutor_test1(self):
        pgm_deliberation_date = datetime(2017, 1, 25)
        dates = {score_encoding.PGM_DELIBERATION_DATE: pgm_deliberation_date,
                 score_encoding.STUDENT_DELIBERATION_DATE: datetime(2017, 1, 27),
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: day_before(pgm_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.PGM_DELIBERATION_DATE})

    def test_get_special_closing_date_for_tutor_test2(self):
        student_deliberation_date = datetime(2017, 1, 22)
        dates = {score_encoding.PGM_DELIBERATION_DATE: datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}

        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})

    def test_get_special_closing_date_for_tutor_test3(self):
        pgm_deliberation_date = datetime(2017, 1, 25)
        dates = {score_encoding.PGM_DELIBERATION_DATE: pgm_deliberation_date,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: day_before(pgm_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.PGM_DELIBERATION_DATE})

    def test_get_special_closing_date_for_tutor_test4(self):
        tutor_closing_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: tutor_closing_date,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: tutor_closing_date,
                          score_encoding.CLOSING_REASON: score_encoding.TUTOR_CLOSING_DATE})

    def test_get_special_closing_date_for_tutor_test5(self):
        student_deliberation_date = datetime(2017, 1, 15)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})

    def test_get_special_closing_date_for_tutor_test6(self):
        tutor_closing_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: datetime(2017, 1, 22),
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: tutor_closing_date,
                          score_encoding.CLOSING_REASON: score_encoding.TUTOR_CLOSING_DATE})

    def test_get_special_closing_date_for_tutor_test7(self):
        tutor_closing_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: datetime(2017, 1, 30),
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: tutor_closing_date,
                          score_encoding.CLOSING_REASON: score_encoding.TUTOR_CLOSING_DATE})

    def test_get_special_closing_date_for_tutor_test8(self):
        legal_date = datetime(2017, 2, 27)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  None,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: legal_date}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: legal_date,
                          score_encoding.CLOSING_REASON: score_encoding.LEGAL_DATE})

    def test_get_special_closing_date_for_tutor_test9(self):
        student_deliberation_date = datetime(2017, 1, 15)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})

    def test_get_special_closing_date_for_tutor_test10(self):
        student_deliberation_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})

    def test_get_special_closing_date_for_tutor_test11(self):
        tutor_closing_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: datetime(2017, 1, 30),
                 score_encoding.TUTOR_CLOSING_DATE: tutor_closing_date,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: tutor_closing_date,
                          score_encoding.CLOSING_REASON: score_encoding.TUTOR_CLOSING_DATE})

    def test_get_special_closing_date_for_tutor_test12(self):
        tutor_closing_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: tutor_closing_date,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, False),
                         {score_encoding.CLOSING_DATE: tutor_closing_date,
                          score_encoding.CLOSING_REASON: score_encoding.TUTOR_CLOSING_DATE})

    def test_get_special_closing_date_for_program_manager_test1(self):
        pgm_deliberation_date = datetime(2017, 1, 25)
        dates = {score_encoding.PGM_DELIBERATION_DATE: pgm_deliberation_date,
                 score_encoding.STUDENT_DELIBERATION_DATE: datetime(2017, 1, 27),
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(pgm_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.PGM_DELIBERATION_DATE})

    def test_get_special_closing_date_for_program_manager_test2(self):
        student_deliberation_date = datetime(2017, 1, 22)
        dates = {score_encoding.PGM_DELIBERATION_DATE: datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
    
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})

    def test_get_special_closing_date_for_program_manager_test3(self):
        pgm_deliberation_date = datetime(2017, 1, 25)
        dates = {score_encoding.PGM_DELIBERATION_DATE: pgm_deliberation_date,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(pgm_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.PGM_DELIBERATION_DATE})

    def test_get_special_closing_date_for_program_manager_test4(self):
        pgm_deliberation_date = datetime(2017, 1, 25)
        tutor_closing_date = datetime(2017, 1, 20)

        dates = {score_encoding.PGM_DELIBERATION_DATE:  pgm_deliberation_date,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: tutor_closing_date,
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(pgm_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.PGM_DELIBERATION_DATE})
    
    def test_get_special_closing_date_for_program_manager_test5(self):
        student_deliberation_date = datetime(2017, 1, 15)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})
    
    def test_get_special_closing_date_for_program_manager_test6(self):
        student_deliberation_date = datetime(2017, 1, 25)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  datetime(2017, 1, 25),
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})
    
    def test_get_special_closing_date_for_program_manager_test7(self):
        pgm_deliberation_date = datetime(2017, 1, 25)
        dates = {score_encoding.PGM_DELIBERATION_DATE: pgm_deliberation_date,
                 score_encoding.STUDENT_DELIBERATION_DATE: datetime(2017, 1, 30),
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(pgm_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.PGM_DELIBERATION_DATE})
    
    def test_get_special_closing_date_for_program_manager_test8(self):
        legal_date = datetime(2017, 2, 27)
        dates = {score_encoding.PGM_DELIBERATION_DATE:  None,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: None,
                 score_encoding.LEGAL_DATE: legal_date}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: legal_date,
                          score_encoding.CLOSING_REASON: score_encoding.LEGAL_DATE})
    
    def test_get_special_closing_date_for_program_manager_test9(self):
        student_deliberation_date = datetime(2017, 1, 15)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})

    def test_get_special_closing_date_for_program_manager_test10(self):
        student_deliberation_date = datetime(2017, 1, 20)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})
    
    def test_get_special_closing_date_for_program_manager_test11(self):
        student_deliberation_date = datetime(2017, 1, 30)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: student_deliberation_date,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: datetime(2017, 2, 27)}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: day_before(student_deliberation_date),
                          score_encoding.CLOSING_REASON: score_encoding.STUDENT_DELIBERATION_DATE})
    
    def test_get_special_closing_date_for_program_manager_test12(self):
        legal_date = datetime(2017, 2, 27)
        dates = {score_encoding.PGM_DELIBERATION_DATE: None,
                 score_encoding.STUDENT_DELIBERATION_DATE: None,
                 score_encoding.TUTOR_CLOSING_DATE: datetime(2017, 1, 20),
                 score_encoding.LEGAL_DATE: legal_date}
        self.assertEqual(score_encoding.get_special_closing_date(dates, True),
                         {score_encoding.CLOSING_DATE: legal_date,
                          score_encoding.CLOSING_REASON: score_encoding.LEGAL_DATE})


def prepare_exam_enrollment_for_double_encoding_validation(exam_enrollment):
    exam_enrollment.score_reencoded = 14
    exam_enrollment.score_draft = 14
    exam_enrollment.save()


def add_permission(user, codename):
    perm = get_permission(codename)
    user.user_permissions.add(perm)


def get_permission(codename):
    return Permission.objects.get(codename=codename)


def day_before(a_date):
    return a_date - timezone.timedelta(days=1)
