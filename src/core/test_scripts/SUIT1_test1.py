### DUMMY TESTS ###

from additional.page_object import base, page


class Test(base.Base):
    num_of_xmls = 1  # say we want to use xml as additional something to our tests

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

        print("[INFO] Sending keys")
        first = self.getFirstMsg()
        name.send_keys(first.get('name', ''))
        email.send_keys(first.get('email', ''))
        msg.send_keys(first.get('msg', ''))
        print("[INFO] OK")


def main():
    test = Test()
    test.run()


if __name__ == "__main__":
    main()
