from Tracker import Holding
from constants import DEFAULT_WAIT_INCREMENT
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
import pandas as pd
import time


# create a class that scrapes bivio
class PorfolioScraper:
    def __init__(self, headless=True, wait_increment=DEFAULT_WAIT_INCREMENT):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)

        self.wait_increment = wait_increment

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
        time.sleep(self.wait_increment * 2)

        # get the holding rows
        holding_soup = bs(self.driver.find_element_by_xpath(
            '//table[@class="s_investments s_table"]/..').get_attribute('innerHTML'), 'html.parser')

        # remove the short part if it exists
        try:
            holding_soup.find('tr', {'class': 'b_title_row'}).extract()
            holding_soup.find_all('tr', {'class': 'b_heading_row'})[
                -1].extract()
        except AttributeError:
            # it has already been extracted
            pass

        # make a df
        holding_df = pd.read_html(str(holding_soup))[0]
        new_columns = {column: column.replace(
            ' ', '') for column in holding_df.columns}

        holding_df.rename(columns=new_columns, inplace=True)

        # get the correct tickers and add them to the df
        holding_df['Ticker'] = [row.text.strip().replace('(', '').replace(')', '')
                                for row in self.driver.find_elements_by_xpath('//tr[@class="b_data_row"]//td[1]//font[@class="s_smaller"]')]

        # use list comp to turn those into holdings
        holdings = [self.add_holding(row)
                    for index, row in holding_df.iterrows()]
        holdings = [holding for holding in holdings if holding]

        date = self.handle_date(holding_df.iloc[0]['ValuationDate'])

        return holdings, date

    # make a
    def add_holding(self, row):
        # get the holding value
        try:
            shares = float(row['SharesHeld'])
            share_price = float(row['PriceperShare'])
        except ValueError:
            # shorts will not work as they have ()
            return None

        ticker = row['Ticker']

        timestamp = self.handle_date(row['ValuationDate'])

        holding = Holding(ticker, shares=shares,
                          share_price=share_price, timestamp=timestamp)

        return holding

    # take the date and make it into a general unix time
    def handle_date(self, date_raw):
        date = date_raw.split('/')
        month = int(date[0])
        day = int(date[1])
        if len(str(date[2])) == 2:
            year = int(f"20{date[2]}")
        elif len(str(date[2])) == 4:
            year = int(date[2])

        unix_time = dt(year, month, day)

        return unix_time

    def quit(self):
        self.driver.quit()
