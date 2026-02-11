"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from api.models import *
from app.forms import *
import sys
from io import StringIO
import subprocess

def home(request):
    """Renders the home page."""


    str = """import unittest
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



unittest.main()"""


    codeOut = StringIO()
    codeErr = StringIO()
 

    # capture output and errors
    sys.stdout = codeOut
    sys.stderr = codeErr
    process = subprocess.Popen(['python', 'manage.py', str])
    exec(str)
    # restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
 
    s = codeErr.getvalue()
    r = codeOut.getvalue()
 
    codeOut.close()
    codeErr.close()






    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def tests(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)   
    tests = Test.objects.all()
    return render(request, 'app/tests.html', {'records': tests})

def test(request,id):
    assert isinstance(request, HttpRequest)   
    test = get_object_or_404(Test, id=id)
    etapes = Etape.objects.filter(test=id)
    return render(request, 'app/test.html', {'test': test,'etapes':etapes})

def createtest(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = CreateTestForm(request.POST)  # Nous reprenons les données

        if form.is_valid(): # Nous vérifions que les données envoyées sont valides

            # Ici nous pouvons traiter les données du formulaire
            titre = form.cleaned_data['url']
            url = form.cleaned_data['nom']          
            r = Record()
            r.titre = titre
            r.url = url
            r.save()
            steps = Step.objects.filter(record=r.id)
            return redirect('app/test.html',{'record': r,'steps':steps})

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = CreateTestForm()  # Nous créons un formulaire vide

    return render(request, 'app/createtest.html', locals())
