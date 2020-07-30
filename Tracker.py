from datetime import timedelta, datetime as dt
from contextlib import contextmanager
import yfinance as yf
import sys
import os


# create a monitor base class
class PriceMonitor:
    # initialize with a ticker
    def __init__(self, ticker):
        self.ticker = ticker
        self.info = yf.Ticker(ticker).info

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


# create a holding class
class Holding(PriceMonitor):
    def __init__(self, ticker, value=None, shares=None, timestamp=dt.now()):
        self.ticker = ticker

        if (not value) and (not shares):
            print('Include a value or share amount to initialize a holding')
            return

        # check for the value and shares
        self.timestamp = timestamp
        self.share_price = self.get_close_price(timestamp)

        if value:
            self.value = value
        else:
            self.value = shares * self.share_price

        if shares:
            self.shares = shares
        else:
            self.shares = self.value / self.share_price

    def set_proportion(self, total_portfolio_value):
        self.proportion = self.value / total_portfolio_value

        return self.proportion

    def update_value(self, date=dt.now()):
        price = self.get_close_price(date)

        self.value = self.shares * price

    def __repr__(self):
        return f"{self.ticker} (Shares: {self.shares})"


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
    # list the tickers
    tickers = ['SPY', 'XLK', 'XLC', 'XLV', 'XLY',
               'XLE', 'XLU', 'XLB', 'XLI', 'MCHI', 'GLD']
    for ticker in tickers:
        with suppress_stdout():
            monitor = PriceMonitor(ticker)
            change = monitor.get_trading_weekly_change()

        print(f"{monitor.info['longName']} ({ticker}): {change}\n")
