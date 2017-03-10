from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from backoffice.management.commands import generate_records_academic_year

url = "http://localhost:8000/"
text_denied = "You're out of the period of scores' encodings : the last exams' session is closed since"


class AccessToProgramDeniedBeforeAcademicYear(StaticLiveServerTestCase):

    def setUpClass(self):
        super(AccessToProgramDeniedBeforeAcademicYear, self).setUpClass()
        self.selenium = WebDriver()
        self.selenium.implicitly_wait(30)
        self.base_url = url
        self.verificationErrors = []
        self.accept_next_alert = True
        generate_records_academic_year.create_academic_year_before()

    def tearDownClass(self):
        self.selenium.quit()
        super(AccessToProgramDeniedBeforeAcademicYear, self).tearDownClass()


    def test_out_of_period_encoding(self):
        pge_depart = self.selenium.get(url) #depart
        if not "OSIS" in self.selenium.title:
            raise Exception("Unable to load OSIS - Encoding module!")
        self.assertEqual(pge_depart.content, b"Students' path")
        self.selenium.find_element_by_id("lnk_home_studies").click()
        self.selenium.find_element_by_id("lnk_assessments").click()
        self.selenium.find_element_by_id("lnk_score_encoding").click()
        assert text_denied not in self.selenium.get(self.selenium.current_url())
        self.selenium.implicitly_wait(5)


    def is_element_present(self, how, what):
        try:
            self.selenium.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try:
            self.selenium.switch_to_alert()
        except NoAlertPresentException as e:
                return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.selenium.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True
