### DUMMY TESTS ###

from additional.page_object import base, page


class Test(base.Base):
    num_of_xmls = 2  # say we want to use xml as additional something to our tests

    def run(self):

        print("[INFO] Launching: %s" % __file__.split('/')[-1].split('.')[0])
        main_page = page.MainPage(self.driver)

        url = self.cfg['ENVIRONMENT']['MAINPAGE']
        print("[INFO] Navigating to %s" % url)
        main_page.navigateTo(url)

        print("[INFO] Clicking Big Page")
        main_page.clickBigPage()

        big_page = page.BigPage(self.driver)
        big_page.createWait()
        name = big_page.getNameEl()
        email = big_page.getEmailEl()
        msg = big_page.getMessageEl()
        username = big_page.getUsernameEl()
        password = big_page.getPasswordEl()
        login = big_page.getLoginEl()

        first = self.getFirstMsg()
        name.send_keys(first.get('name', ''))
        email.send_keys(first.get('email', ''))
        msg.send_keys(first.get('msg', ''))

        second = self.getSecondMsg()
        username.send_keys(second.get('username', ''))
        password.send_keys(second.get('password', ''))
        print("[INFO] Clicking login")
        login.click()

        print("[INFO] Checking if login is successful")
        login_page_result = page.LoginPageResult(self.driver)
        result = login_page_result.isLoginSuccess()
        print("[INFO] Result: %s" % result)


def main():
    test = Test()
    test.run()


if __name__ == "__main__":
    main()
