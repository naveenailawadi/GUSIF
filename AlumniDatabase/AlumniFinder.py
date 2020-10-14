from constants import DEFAULT_WAIT_INCREMENT
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import time


# create a class that logs into linkedin
class LinkedInBot:
    def __init__(self, headless=False, wait_increment=DEFAULT_WAIT_INCREMENT):
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument('--headless')

        self.driver = webdriver.Firefox(options=options)

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

    # make a function to connect with people
    def connect(self, linkedin_url):
        self.driver.get(linkedin_url)

        time.sleep(self.wait_increment)

        # get the connect button
        connect_btn = None
        try:
            connect_btn = self.driver.find_element_by_xpath(
                '//button[@class="pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view"]')
        except NoSuchElementException:
            pass

        if not connect_btn:
            # click more
            try:
                more_btn = self.driver.find_element_by_xpath(
                    '//button[@class="ml2 pv-s-profile-actions__overflow-toggle artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view"]')
            except NoSuchElementException:
                return  # no profile here

            more_btn.click()

            # find connect here
            time.sleep(self.wait_increment)

            try:
                connect_btn = self.driver.find_element_by_xpath(
                    '//div[@class="pv-s-profile-actions pv-s-profile-actions--connect pv-s-profile-actions__overflow-button full-width text-align-left artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view"]')
            except NoSuchElementException:
                print(f"Already connected with {linkedin_url}")

        # click connect
        if connect_btn:
            connect_btn.click()
            time.sleep(self.wait_increment)

            # click done
            done_btn = self.driver.find_element_by_xpath(
                '//button[@class="ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view"]')
            done_btn.click()
            time.sleep(self.wait_increment)

    # quit the driver
    def quit(self):
        self.driver.quit()


# create a class that add PDL data
class DataExtender:
    # initialize with a PDL key
    def __init__(self, pdl_key):
        # this root will be used through most functions
        self.root = f"https://api.peopledatalabs.com/v5/person?pretty=true&api_key={pdl_key}&"

    # create a function that constructs a linkedin request
    def create_profile_request(self, first_name, last_name, linkedin_profile, school="Georgetown University"):
        params = {
            'first_name': first_name,
            'last_name': last_name,
            'profile': linkedin_profile
        }

        if school:
            params['school'] = school

        return params

    # this gets the general data for some json
    def get_data(self, params):
        raw = requests.get(self.root, params=params)
        if '200' in str(raw):
            print('Request successful')
            data = raw.json()['data']
        elif '400' in str(raw):
            data = None
        else:
            data = None

        return data

    # create an integrated request for a linkedin profile with name splitting
    def extend_alum(self, first_name, last_name, linkedin_profile, school="Georgetown University"):
        params = self.create_profile_request(
            first_name, last_name, linkedin_profile, school=school)

        # get the data
        data = self.get_data(params)

        # check if there is data
        if not data:
            return None

        # get the important data
