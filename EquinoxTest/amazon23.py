import unittest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


class idUserAndIdTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.currentResult = None
		cls.driver = WebDriver("http://longchicken.cloudapp.net:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)
		cls.driver.get('http://www.amazon.fr/')
		cls.driver.set_window_size(1920,1080)
		cls.driver.implicitly_wait(10)

	def run(self, result=None):
		self.currentResult = result # remember result for use in tearDown
		unittest.TestCase.run(self, result) # call superclass run method

	def test_sequence1(self):
		actions = ActionChains(self.driver)
		elem = self.driver.find_element_by_css_selector('#twotabsearchtextbox')
		actions.move_to_element(elem)
		actions.click()
		actions.perform()

	def test_sequence2(self):
		actions = ActionChains(self.driver)
		elem = self.driver.find_element_by_css_selector('#twotabsearchtextbox')
		actions.move_to_element(elem)
		actions.click()
		actions.send_keys('ordinateur')
		actions.perform()

	def test_sequence3(self):
		actions = ActionChains(self.driver)
		elem = self.driver.find_element_by_css_selector('#issDiv3')
		actions.move_to_element(elem)
		actions.click()
		actions.perform()

	def test_sequence4(self):
		actions = ActionChains(self.driver)
		elem = self.driver.find_element_by_css_selector('#result_0 > div > div > div > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h2')
		actions.move_to_element(elem)
		actions.click()
		actions.perform()

	def test_sequence5(self):
		actions = ActionChains(self.driver)
		elem = self.driver.find_element_by_css_selector('#centerCol')
		actions.move_to_element(elem)
		actions.click()
		actions.perform()

	@classmethod
	def tearDownClass(cls):
		cls.driver.close()
		ok = cls.currentResult.wasSuccessful()
		errors = cls.currentResult.errors
		failures = cls.currentResult.failures
		print(' All tests passed so far!' if ok else \
			' %d errors and %d failures so far' % \
			(len(errors), len(failures)))


if __name__ == "__main__":
	unittest.main()