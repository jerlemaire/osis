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
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10

class LearningUnitsSearchTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def error_displayed(self,error_msg):
        start_time = time.time()
        while True:
            try:
                error_invalid_search= self.browser.find_element_by_class_name('error').text
                self.assertEqual(_(error_msg), error_invalid_search)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def go_home_page(self):
        start_time = time.time()
        while True:
            try:
                self.assertIn('OSIS', self.browser.title)
                header_text = self.browser.find_element_by_tag_name('h1').text
                self.assertIn('Log-in', header_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def go_learning_units_page(self):
        # She goes on the homepage to log in
        self.browser.get('http://127.0.0.1:8000/')  # We should use : self.live_server_url
        self.go_home_page()

        # She is invited to log in
        self.user_logs_in('defat','osis')

        # She goes in the header menu and clicks on 'Formation Catalogue'
        # and then 'Learning Units' to go on the search page of learning units.
        self.browser.get('http://127.0.0.1:8000/learning_units/')
        # She notices the title of the learning units search page
        self.wait_for_tag('h2','learning_units')

    def user_logs_in(self, usr, pwd):
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
        inputbox_login_usr.send_keys(usr)
        inputbox_login_pwd.send_keys(pwd)
        login_button = self.browser.find_element_by_id('post_login_btn')
        login_button.send_keys(Keys.ENTER)
        start_time = time.time()
        while True:
            try:
                dropdown_text = self.browser.find_element_by_id('lnk_home_dropdown_catalog').text
                self.assertEqual(_('formation_catalogue'), dropdown_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('table_learning_units')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_cols_in_list_table(self, col_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('table_learning_units')
                cols = table.find_elements_by_tag_name('td')
                self.assertIn(col_text, [col.text for col in cols])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for_tag(self,tag_name,tag_value):
        start_time = time.time()
        while True:
            try:
                header_text = self.browser.find_element_by_tag_name(tag_name).text
                self.assertEqual(_(tag_value), header_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        self.browser.quit()

    def test_retrieve_learning_units_from_search_with_valid_acronym_only(self):
        # Sarah needs to check out an existing learning_unit
        self.go_learning_units_page()

        # She enters a valid acronym only,
        # to see if a learning unit exists in a particular year.
        inputbox_acronym=self.browser.find_element_by_id('id_acronym')
        inputbox_acronym.send_keys('DROI1212')

        # Then she start the search
        login_button= self.browser.find_element_by_id('bt_submit_learning_unit_search')
        login_button.send_keys(Keys.ENTER)

        #She now can see the response returned by the application
        self.wait_for_cols_in_list_table('DROI1212')

        # She sees that this acronym already exists and the corresponding class is still valid for a particular year
        # Satisfied, she logs out.

    def test_error_when_search_has_no_input_value_given_by_user(self):
        # Sarah needs to check out an existing learning_unit
        self.go_learning_units_page()

        # She starts a search by pressing ENTER by mistake,
        # without entering any input values
        login_button= self.browser.find_element_by_id('bt_submit_learning_unit_search')
        login_button.send_keys(Keys.ENTER)

        # She sees an error when the page refreshes
        self.error_displayed('LU_ERRORS_INVALID_SEARCH')

        # Unhappy of the situation, she closes the browser...

    def test_error_when_search_has_invalid_acronym_and_no_academic_year_given_by_user(self):
        # Sarah needs to check out an existing learning_unit
        self.go_learning_units_page()

        # She enters a non-valid acronym and doesnt specify an academic year,
        # to see if a learning unit exists in a particular year.
        inputbox_acronym=self.browser.find_element_by_id('id_acronym')
        inputbox_acronym.send_keys('DROI12')

        # She starts a search by pressing ENTER
        login_button= self.browser.find_element_by_id('bt_submit_learning_unit_search')
        login_button.send_keys(Keys.ENTER)

        # She sees an error when the page refreshes
        self.error_displayed('LU_ERRORS_YEAR_WITH_ACRONYM')

        # Unhappy of the situation, she closes the browser...

    def test_error_when_search_has_no_acronym_and_no_academic_year_given_by_user(self):
        # Sarah needs to check out an existing learning_unit
        self.go_learning_units_page()

        # She enters a keyword only and doesnt specify an academic year,
        # to see if a learning unit exists in a particular year.
        inputbox_keyword=self.browser.find_element_by_id('id_keyword')
        inputbox_keyword.send_keys('droit')

        # She starts a search by pressing ENTER
        login_button= self.browser.find_element_by_id('bt_submit_learning_unit_search')
        login_button.send_keys(Keys.ENTER)

        # She sees an error when the page refreshes
        self.error_displayed('LU_ERRORS_ACADEMIC_YEAR_REQUIRED')

        # Unhappy of the situation, she closes the browser...

    def test_error_when_search_has_academic_year_but_no_other_input_value_given_by_user(self):
        # Sarah needs to check out an existing learning_unit
        self.go_learning_units_page()

        # She enters a keyword only and doesnt specify an academic year,
        # to see if a learning unit exists in a particular year.
        # navigate to the page
        academic_year = Select(self.browser.find_element_by_id('slt_academic_year'))
        #print ([ay.text for ay in academic_year.options])
        academic_year.select_by_visible_text('2016-2017')

        # She starts a search by pressing ENTER
        login_button= self.browser.find_element_by_id('bt_submit_learning_unit_search')
        login_button.send_keys(Keys.ENTER)

        # She sees an error when the page refreshes
        self.error_displayed('LU_ERRORS_INVALID_SEARCH')

        # Unhappy of the situation, she closes the browser...