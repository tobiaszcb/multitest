from selenium.webdriver.common.by import By


class MainPageLocator:
    BIG_PAGE = (By.XPATH, "//a[text()='Big page with many elements']")


class BigPageLocator:
    NAME = (By.ID, "et_pb_contact_name_0")
    EMAIL_ADDRESS = (By.ID, "et_pb_contact_email_0")
    MESSAGE = (By.ID, "et_pb_contact_message_0")

    USERNAME = (By.XPATH, "//input[@placeholder='Username']")
    PASSWORD = (By.XPATH, "//input[@placeholder='Password']")
    LOGIN = (By.XPATH, "//button[text()='Login']")
