### DUMMY TESTS ###

from abc import ABC, abstractmethod
import os, sys
import configparser
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import xml.etree.ElementTree as ET

from selenium.webdriver.support.wait import WebDriverWait


class BasePage:

    def __init__(self, driver):
        self.driver = driver

class Base(ABC):
    """Base Class"""

    def __init__(self):
        self.driver, self.cfg = self.setUp()

    def __del__(self):
        self.driver.quit()

    def setUp(self):
        return self.createWebdriver(), self.getCfg()

    def getCfg(self):
        cfg = configparser.ConfigParser()
        cfg.read(sys.argv[1])
        return cfg

    def createWebdriver(self):
        options = Options()
        if 'NOHEADLESS' not in os.environ:
            options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)
        return driver

    def getFirstMsg(self) -> dict:
        xmlDict = self._getXmlsContentAsDict()
        return xmlDict.get('first', None)

    def getSecondMsg(self) -> dict:
        xmlDict = self._getXmlsContentAsDict()
        return xmlDict.get('second', None)

    def _getXmlsContentAsDict(self) -> dict:
        xmls = self._getXmls()
        xmlDict = {}
        if len(xmls) != 0:
            root1 = xmls[0]
            xmlDict.update({
                'first': {
                    'name': root1.find('name').text,
                    'email': root1.find('email').text,
                    'msg': root1.find('msg').text
                }
            })
            if len(xmls) == 2:
                root2 = xmls[1]
                xmlDict.update({
                    'second': {
                        'username': root2.find('username').text,
                        'password': root2.find('password').text
                    }
                })
        return xmlDict

    def _getXmls(self):
        xmls = []
        if self.num_of_xmls != 0:
            xmls.append(ET.parse(sys.argv[2]))
            if self.num_of_xmls == 2:
                xmls.append(ET.parse(sys.argv[3]))
        return xmls


    @abstractmethod
    def run(self):
        pass
