from constants import DEFAULT_WAIT_INCREMENT
from AlumniDatabase.secrets import LINKEDIN_USERNAME, LINKEDIN_PASSWORD
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import sys


# create a class that logs into linkedin
class LinkedInBot:
    def __init__(self, headless=False, wait_increment=DEFAULT_WAIT_INCREMENT):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)

        self.wait_increment = wait_increment

    # login
    def login(self, username, password):
        self.driver.get('https://www.linkedin.com/')

        # send keys to username and password boxes
        username_box = self.driver.find_element_by_xpath(
            '//input[@autocomplete="username"]')
        time.sleep(self.wait_increment)
        username_box.send_keys(username)

        password_box = self.driver.find_element_by_xpath(
            '//input[@autocomplete="current-password"]')
        time.sleep(self.wait_increment)
        password_box.send_keys(password)

        password_box.send_keys(Keys.ENTER)
        time.sleep(2 * self.wait_increment)

    # find the best match for a search term (returns a linkedin profile)
    def find_best_match(self, search_term):
        # send the search to the search box
        search_box = self.driver.find_element_by_xpath(
            '//input[@placeholder="Search"]')

        # delete all the info inside
        search_box.clear()

        # send the new search
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5 * self.wait_increment)

        # get the top entry
        try:
            top_entry = self.driver.find_element_by_xpath(
                '//div[@class="search-result__wrapper"]')

            # get the profile url
            profile = top_entry.find_element_by_xpath(
                '//a[@data-control-name="search_srp_result"]').get_attribute('href')
        except NoSuchElementException:
            profile = 'N/A'

        # return the linkedin profile
        return profile

    # quit the driver
    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    # import the dataset from a command line arg
    data = sys.argv[1].strip().replace('\\', '')

    # load the data into pandas
    df = pd.read_csv(data)

    # create a bot (and login)
    bot = LinkedInBot()
    bot.login(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    input('Click enter when captcha is broken')

    # iterate over all the rows of the df
    for index, row in df.iterrows():
        # get the necessary data
        name = row['Name']
        profile = row['LinkedIn Profile']

        # search the term if there is no profile yet
        if pd.isnull(profile):
            print(f"Checking data for {name}")
            search = f"{name} Georgetown"
            new_profile = bot.find_best_match(search)
            df.loc[index, 'LinkedIn Profile'] = new_profile

            df.to_csv(data, index=False)

    bot.quit()

    #
