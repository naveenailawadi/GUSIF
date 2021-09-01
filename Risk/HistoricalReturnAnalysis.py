from statistics import geometric_mean
import requests
import pandas as pd
import numpy as np
import time
import os

# create a folder where you will keep all the downloaded information
DEFAULT_DOWNLOAD_FOLDER = "Risk/HistoricalReturns"

# set a default wait time
DEFAULT_WAIT_TIME = 5

# set the trading days in a year
TRADING_DAYS = 252

# make a header
USER_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}


# make a class that holds a holding df
class AnalyzedHolding:
    def __init__(self, data_file):
        # open the data file
        self.df = pd.read_csv(data_file)

        self.ticker = data_file.split('.')[0].split('/')[-1]

        # add a daily return column
        self.df['Daily Return'] = np.log(
            self.df['Adj Close'] / self.df['Open'])

        self.df['1 + Daily Return'] = 1 + self.df['Daily Return']

        # save key start and close prices
        self.start_price = self.df['Open'][0]
        self.end_price = self.df['Adj Close'].tail(1).item()

    # make an overall HPR
    @property
    def hpr(self):
        hpr = (self.end_price - self.start_price) / self.start_price
        return hpr

    # make an arithmetic average daily return
    @property
    def arithmetic_average_daily_return(self):
        avg = np.average(self.df['Daily Return'])

        return avg

    # make a geometric average
    @property
    def geometric_average_daily_return(self):
        avg = geometric_mean(self.df['1 + Daily Return']) - 1

        return avg

    # make an arithmetic average annualized return
    @property
    def arithmetic_average_annualized_return(self):
        avg = TRADING_DAYS * self.arithmetic_average_daily_return

        return avg

    # make a geometric average annualized return
    @property
    def geometric_average_annualized_return(self):
        avg = TRADING_DAYS * self.geometric_average_daily_return

        return avg

    # make daily return standard deviation
    @property
    def daily_return_stdev(self):
        stdev = np.std(self.df['Daily Return'])

        return stdev

    # make an annualized return standard deviation
    @property
    def annualized_return_stdev(self):
        stdev = self.daily_return_stdev * np.sqrt(TRADING_DAYS)

        return stdev


# make a returns analyzer class
class ReturnsDataHandler:
    # make a function to get the historical returns of one stock
    # period start and end are in seconds
    def get_daily_returns(self, ticker, period_start, period_end, download_folder=DEFAULT_DOWNLOAD_FOLDER, wait_time=DEFAULT_WAIT_TIME):
        # make the url
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period_start}&period2={period_end}&interval=1d&events=history&includeAdjustedClose=true"

        # make an outfile
        outfile = f"{download_folder}/{ticker}.csv"

        # request the data from the url
        raw = requests.get(url, headers=USER_HEADER, timeout=5)

        # save if there is the right status
        if raw.status_code == 200:
            with open(outfile, 'wb') as outfile:
                outfile.write(raw.content)
        else:
            print(
                f"Failed to download data for {ticker}, waiting {wait_time} seconds")
            time.sleep(wait_time)

    # make a function that gets all the current companies in the folder
    def current_tickers(self, download_folder=DEFAULT_DOWNLOAD_FOLDER):
        # get all the files
        files = [f for f in os.listdir(download_folder) if os.path.isfile(
            os.path.join(download_folder, f))]

        # format the files into tickers
        tickers = [file.split('.')[0] for file in files]

        return tickers


'''
NOTES
- sample URL for csv download
https://query1.finance.yahoo.com/v7/finance/download/NFLX?period1=1609459200&period2=1630368000&interval=1d&events=history&includeAdjustedClose=true
'''
