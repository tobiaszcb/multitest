### DUMMY TESTS ###

from additional.page_object import base, page
import time

#from src.core.test_scripts.page_object import page, base


class Test(base.Base):
    num_of_xmls = 0  # say we want to use xml as additional something to our tests

    def run(self):

        print("[INFO] Launching: %s" % __file__.split('/')[-1].split('.')[0])
        main_page = page.MainPage(self.driver)

        url = self.cfg['ENVIRONMENT']['MAINPAGE']
        print("[INFO] Navigating to %s" % url)
        main_page.navigateTo(url)

        print("[INFO] Clicking Big Page")
        main_page.clickBigPage()
        time.sleep(5)

        big_page = page.BigPage(self.driver)
        big_page.createWait()
        time.sleep(5)

        print("[INFO] Checking if login is successful")
        login_page_result = page.LoginPageResult(self.driver)
        result = login_page_result.isLoginSuccess()
        print("[INFO] Result: %s" % result)


def main():
    test = Test()
    test.run()


if __name__ == "__main__":
    main()
