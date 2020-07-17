from datetime import timedelta, datetime as dt
from contextlib import contextmanager
import yfinance as yf
import sys
import os


# list the tickers
TICKERS = ['XLK', 'XLC', 'XLV', 'XLY', 'XLE', 'XLU', 'XLB', 'XLI']


# create a trading period class
class TradingPeriod:
    def __init__(self, start_date, start_price, end_date, end_price):
        self.start_date = start_date
        self.start_price = start_price
        self.end_date = end_date
        self.end_price = end_price

    # return the percent change as a decimal
    def percent_change(self):
        change = (self.end_price - self.start_price) / self.start_price

        return change

    def time_elapsed(self):
        diff = self.end_date - self.start_date
        return diff.days

    def __repr__(self):
        return f"{round(100 * self.percent_change(), 2)}% ({self.time_elapsed()})"


class PriceMonitor:
    # initialize with a ticker
    def __init__(self, ticker):
        self.ticker = ticker

    # create a function to get the change over the last trading week
    def get_trading_weekly_change(self):
        today = dt.now()

        # get start
        start_date = today - timedelta(days=today.weekday())
        print(start_date)
        start_price = self.get_open_price(start_date)

        # get end
        end_price = self.get_close_price(today)

        # return a trading period
        period = TradingPeriod(start_date, start_price, today, end_price)
        return period

    def get_open_price(self, date):
        data = yf.download(self.ticker, start=(
            date - timedelta(days=3)), end=date)

        print(data)

        price = float(data.iloc[[-1]]['Open'])

        return price

    def get_close_price(self, date):
        data = yf.download(self.ticker, start=(
            date - timedelta(days=3)), end=date)

        # get closing price
        price = float(data.iloc[[-1]]['Close'])

        return price


# suppress the output for cleanliness
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


if __name__ == '__main__':
    for ticker in TICKERS:
        with suppress_stdout():
            monitor = PriceMonitor(ticker)
            change = monitor.get_trading_weekly_change()

        print(f"{ticker}: {change}\n")
