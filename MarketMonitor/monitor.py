from forex_python.converter import CurrencyRates, CurrencyCodes
from selenium import webdriver
import time


SLEEP_INCREMENT = 2


class ForexMonitor(CurrencyRates, CurrencyCodes):
    # create a function to compare based on a set forx
    def usd_to(self, symbol):
        # get rate
        rate = round(self.get_rate('USD', symbol), 2)

        other_symbol = self.get_symbol(symbol)
        return f"$1 : {other_symbol}{rate}"


class CommodityMonitor:
    # get the price of gold
    def get_gold_price(self):
        driver = create_driver()
        driver.get('https://www.monex.com/gold-prices/')
        time.sleep(SLEEP_INCREMENT)

        # get the gold price
        gold_price_raw = driver.find_element_by_xpath(
            '//td[@id="spotoz"]').text
        gold_price = f"Gold: {gold_price_raw} (per ounce)"
        driver.quit()

        # return the gold price
        return gold_price

    # get the price of oil in dollars
    def get_wti_price(self):
        # use selenium (better for interacting with JS)
        driver = create_driver()
        driver.get('https://oilprice.com/oil-price-charts')
        time.sleep(SLEEP_INCREMENT)

        # get the oil price
        wti_price_raw = driver.find_element_by_xpath(
            '//tr[@data-spreadsheet="Crude Oil WTI"]//td[@class="last_price"]').text
        wti_price = f"WTI Oil: ${wti_price_raw} (per barrel)"
        driver.quit()

        return wti_price


# create a class for getting bond prices
class BondMonitor:
    def get_yield(self, year_amount):
        driver = create_driver()
        driver.get(
            f"https://ycharts.com/indicators/{year_amount}_year_treasury_rate")
        time.sleep(SLEEP_INCREMENT)
        rate = driver.find_element_by_xpath(
            '//div[@id="pgNameVal"]').text.split(' ')[0]
        driver.quit()

        return rate


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1420,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver


'''
NOTES
- this monitors the forex and oil markets and pushes data via telegram
'''
