from Tracker import Holding
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


# create a class that scrapes bivio
class PorfolioScraper:
    def __init__(self, headless=True):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)

    def login(self, username, password):
        bivio_login_site = 'https://www.bivio.com/my-club-site'
        self.driver.get(bivio_login_site)

        # send the keys to the username and password fields
        username_box = self.driver.find_element_by_xpath(
            '//input[@type="text"]')
        username_box.send_keys(username)

        password_box = self.driver.find_element_by_xpath(
            '//input[@type="password"]')
        password_box.send_keys(password)

        # click enter
        password_box.send_keys(Keys.ENTER)

    # make a function that returns all the holdings as holdings objects
    def scrape_holdings(self):
        holdings_site = 'https://www.bivio.com/gtowninvestors/accounting/investments'
        self.driver.get(holdings_site)

        # get the holding rows
        holding_rows = self.driver.find_elements_by_xpath(
            '//tr[@class="b_data_row"]')

        # use list comp to turn those into holdings
        holdings = [self.add_holding(row) for row in holding_rows]

    def add_holding(self, holding_row_element):

    def quit(self):
        self.driver.quit()
