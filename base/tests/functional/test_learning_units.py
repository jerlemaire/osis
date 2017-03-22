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
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################

from django.utils.translation import ugettext_lazy as _
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class LearningUnitsSearchTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_retrieve_learning_units_from_search_with_valid_acronym_only(self):
        # Sarah needs to check out an existing learning_unit
        # She goes on the homepage to log in
        self.browser.get('http://127.0.0.1:8000/')

        # She notices the page title 'OSIS' and the log in page
        self.assertIn('OSIS', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Log-in', header_text)

        # She is invited to log in
        inputbox_login_usr = self.browser.find_element_by_id('id_username')
        self.assertEqual(
            inputbox_login_usr.get_attribute('placeholder'),
            _('user')
        )
        inputbox_login_pwd = self.browser.find_element_by_id('id_password')
        self.assertEqual(
            inputbox_login_pwd.get_attribute('placeholder'),
            _('password')
        )

        # She logs in
        inputbox_login_usr.send_keys('defat')
        inputbox_login_pwd.send_keys('osis')
        login_button= self.browser.find_element_by_id('post_login_btn')
        login_button.send_keys(Keys.ENTER)
        time.sleep(1)

        # She goes in the header menu and clicks on 'Formation Catalogue'
        # and then 'Learning Units' to be on the search page of learning units
        # She notices the title of the learning units search page
        self.browser.get('http://127.0.0.1:8000/learning_units/')
        header_text = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(_('learning_units'), header_text)

        # She enters a valid acronym only,
        # to see if a learning unit exists in a particular year.
        inputbox_acronym=self.browser.find_element_by_id('id_acronym')
        inputbox_acronym.send_keys('DROI1212')
        # Then she start the search
        login_button= self.browser.find_element_by_id('bt_submit_learning_unit_search')
        login_button.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element_by_id('table_learning_units')
        cols = table.find_elements_by_tag_name('td')
        self.assertIn('DROI1212', [cols.text for cols in cols])
        # She sees that this acronym already exists and the corresponding class is still valid for a particular year
        # Satisfied, she logs out.


    #def test_error_when_search_has_no_input_value_given_by_user(self):


    #def test_error_when_search_has_no_academic_year_given_by_user(self):


    #def test_error_when_search_has_academic_year_but_no_other_input_value_given_by_user(self):


    #def test_search_with_academic_year_and_acronym_valid_only_returns_nothing_then_user_can_add_new_learning_unit(self):


if __name__ == '__main__':
    unittest.main(warnings='ignore')