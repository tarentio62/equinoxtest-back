from io import StringIO
from selenium.webdriver.common.keys import Keys

class JsonStep:
    def __init__(self, _json, target, cmd, value, sequence):
        self.Dicokeys = {13: Keys.ENTER, 9: Keys.TAB}
        self.Json = _json
        self.Action = target
        self.Command = cmd
        self.Value = value
        self.Sequence = sequence
        self.EventCmd = {
            "mouseup": "\t\tactions.move_to_element(elem)\n\t\tactions.click()\n",
            "change": "\t\tactions.move_to_element(elem)\n\t\tactions.click()\n\t\tactions.send_keys('{kwargs}')\n",
            "keydown": "\t\tactions.send_keys('{kwarg}')\n"
        }
        self.MethodScript = StringIO()

    def build_method(self):
        self.MethodScript.write("\n\tdef test_sequence" + str(self.Sequence) + "(self):\n")
        self.MethodScript.write("\t\tactions = ActionChains(self.driver)\n")
        self.MethodScript.write("\t\telem = self.driver.find_element_by_css_selector('" + self.Action + "')\n")
        if self.Command == "change":
            self.MethodScript.write(self.EventCmd[self.Command].format(kwargs=(self.Value)))
        elif self.Command == "keydown":
            self.MethodScript.write(self.EventCmd[self.Command].format(kwargs=(self.Dicokeys[self.Value])))
        else:
            self.MethodScript.write(self.EventCmd[self.Command])
        self.MethodScript.write("\t\tactions.perform()\n")


class SeleniumBuilder:
    def __init__(self, testObj):
        self.Test = testObj

        self.PythonScript = StringIO()

    def create_header(self):
        self.PythonScript.write("import unittest\n")
        self.PythonScript.write("from selenium.webdriver.remote.webdriver import WebDriver\n")
        self.PythonScript.write("from selenium.webdriver.common.desired_capabilities import DesiredCapabilities\n")
        self.PythonScript.write("from selenium.webdriver.common.keys import Keys\n")
        self.PythonScript.write("from selenium.webdriver.common.action_chains import ActionChains\n")
        self.PythonScript.write("from selenium.common.exceptions import NoSuchElementException\n\n\n")

        self.PythonScript.write("class idUserAndIdTest(unittest.TestCase):\n")
        self.PythonScript.write("\t@classmethod\n")
        self.PythonScript.write("\tdef setUpClass(cls):\n")
        self.PythonScript.write('\t\tcls.driver = WebDriver("http://longchicken.cloudapp.net:4444/wd/hub",desired_capabilities=DesiredCapabilities.CHROME)\n')
        self.PythonScript.write("\t\tcls.driver.get('" + self.Test.urlDepart + "')\n")
        self.PythonScript.write("\t\tcls.driver.set_window_size(1920,1080)\n")
        self.PythonScript.write("\t\tcls.driver.implicitly_wait(10)\n")

    def create_methods(self):
        sequence = 0
        for stepJs in self.Test.etapes:
            jstep = JsonStep(stepJs, stepJs.cible, stepJs.commande, stepJs.valeur, stepJs.sequence)
            jstep.build_method()
            self.PythonScript.write(jstep.MethodScript.getvalue())

    def create_footer(self):
        self.PythonScript.write("\n\t@classmethod\n")
        self.PythonScript.write("\tdef tearDownClass(cls):\n")
        self.PythonScript.write("\t\tcls.driver.quit()\n\n\n")
        self.PythonScript.write("""if __name__ == "__main__":\n""")
        self.PythonScript.write("\tunittest.main()\n")

    def obtenir_script(self):
        self.create_header()
        self.create_methods()
        self.create_footer()
        return self.PythonScript.getvalue()

    def save_script(self):
        file = open("testUnit.py", "w", encoding='utf-8')
        file.write(self.PythonScript.getvalue())
        file.close()

