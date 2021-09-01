from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime as dt
import time

# make a main function and get everything
def main():
    # make the driver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # get the url
    driver.get('https://www.ishares.com/us/products/239710/ishares-russell-2000-etf#Holdings')
    time.sleep(5)

    # click to get all the holdings
    all_holdings_btn = driver.find_elements_by_xpath('//a[@class="toggle-records"]')[1]
    ActionChains(driver).move_to_element(all_holdings_btn).perform()
    time.sleep(2)
    all_holdings_btn.click()
    time.sleep(5)

    # get all the holdings
    holding_elems = driver.find_elements_by_xpath('//td[@class=" colTicker col1"]')

    # convert them to text
    tickers = [elem.text for elem in holding_elems]

    # drop them into a pandas df
    df = pd.DataFrame({'tickers': tickers})

    # export the dataframe to a file
    date = dt.now()
    df.to_csv(f"Russell2000_{date.month}_{date.day}.csv", index=False)

    # close the driver
    driver.close()

if __name__ == '__main__':
    main()
