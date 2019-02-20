from .locators import MainPageLocator, BigPageLocator
from .base import BasePage
from .element import BasePageElement
from selenium.webdriver.support.wait import WebDriverWait

# from src.core.test_scripts.page_object.base import BasePage
# from src.core.test_scripts.page_object.element import BasePageElement
# from src.core.test_scripts.page_object.locators import MainPageLocator, BigPageLocator


class LoginPageElement(BasePageElement):
    locator = "login_error"


class MainPage(BasePage):

    def navigateTo(self, url):
        self.driver.get(url)

    def clickBigPage(self):
        button = self.driver.find_element(*MainPageLocator.BIG_PAGE)
        button.click()


class BigPage(BasePage):

    def createWait(self):
        self.wait = WebDriverWait(self.driver, 30)

    def getNameEl(self):
        return self.wait.until(lambda driver: self.driver.find_element(*BigPageLocator.NAME))

    def getEmailEl(self):
        return self.wait.until(lambda driver: self.driver.find_element(*BigPageLocator.EMAIL_ADDRESS))

    def getMessageEl(self):
        return self.wait.until(lambda driver: self.driver.find_element(*BigPageLocator.MESSAGE))

    def getUsernameEl(self):
        return self.wait.until(lambda driver: self.driver.find_element(*BigPageLocator.USERNAME))

    def getPasswordEl(self):
        return self.wait.until(lambda driver: self.driver.find_element(*BigPageLocator.PASSWORD))

    def getLoginEl(self):
        return self.wait.until(lambda driver: self.driver.find_element(*BigPageLocator.LOGIN))


class LoginPageResult(BasePage):
    login_page_element = LoginPageElement()

    def isLoginSuccess(self):
        return not "ERROR" in self.driver.page_source
