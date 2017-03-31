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

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import ugettext_lazy as _
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException
from base.tests.factories.academic_year import AcademicYearFakerFactory
from base.tests.factories.learning_unit_year import LearningUnitYearFakerFactory
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

MAX_WAIT = 10


class LearningUnitsSearchTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1280, 720)

        User.objects.create_superuser(username='superdummy',
                                 email='superdummy@dummy.com',
                                password='superpassword')

    def error_displayed(self,error_msg):
        self.wait_for(lambda: self.browser.find_element_by_class_name('error').is_displayed())

    def go_to_learning_units_page(self):
        # She goes on the homepage to log in
        self.browser.get(self.live_server_url)
        self.wait_for(lambda: self.assertIn('Log-in',self.browser.find_element_by_tag_name('h1').text))

        # She is invited to log in
        self.the_user_logs_in()

        # She goes in the header menu and clicks on 'Formation Catalogue'
        # and then 'Learning Units' to go on the search page of learning units.
        self.browser.get(self.live_server_url+'/learning_units/')
        # She notices the title of the learning units search page
        self.wait_for(lambda: self.browser.find_element_by_tag_name('h2').is_displayed())

    def the_user_logs_in(self):
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
        inputbox_login_usr.send_keys('superdummy')
        inputbox_login_pwd.send_keys('superpassword')
        login_button = self.browser.find_element_by_id('post_login_btn')
        login_button.send_keys(Keys.ENTER)
        ## Wait for the home_page to load on screen
        self.wait_for(lambda:self.browser.find_element_by_id('lnk_home_dropdown_catalog').is_displayed())

    def wait_for_text_in_table(self, table_id, text_to_find, row_or_col):
        self.wait_for(lambda:self.assertIn(text_to_find, [element.text for element in self.browser.find_element_by_id(table_id).find_elements_by_tag_name(row_or_col)]))

    def wait_for(self, fct):
        start_time = time.time()
        while True:
            try:
                return fct()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    self.browser.save_screenshot('screenshot.png')
                    print('BROWSER_GET_LOG: '+str(self.browser.get_log('har')))
                    print('BROWSER_GET_HTML: '+str(self.browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")))
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        self.browser.quit()