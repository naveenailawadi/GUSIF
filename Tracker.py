from datetime import timedelta, datetime as dt
from contextlib import contextmanager
import yfinance as yf
import sys
import os

DAY_DISTANCE = 3


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
            date - timedelta(days=DAY_DISTANCE)), end=date)

        price = float(data.iloc[[-1]]['Open'])

        return price

    def get_close_price(self, date):
        data = yf.download(self.ticker, start=(
            date - timedelta(days=DAY_DISTANCE)), end=date)

        # get closing price
        price = float(data.iloc[[-1]]['Close'])

        return price

    def get_returns_on_timeframe(self, start_date, end_date, absolute=False):
        # get the close prices for both dates
        try:
            start_price = float(self.get_open_price(start_date))
        except IndexError:
            print(f"Trouble with price for {self.ticker}")
            return None, None

        end_price = float(self.get_close_price(end_date))

        # get the return
        absolute_returns = end_price - start_price
        percent_returns = absolute_returns / start_price

        return absolute_returns, percent_returns


# create a holding class
class Holding(PriceMonitor):
    def __init__(self, ticker, value=None, shares=None, share_price=None, timestamp=dt.now(), sector=None):
        # set the ticker and timestamp
        self.ticker = ticker
        self.timestamp = timestamp
        self.sector = sector

        if value or shares:

            # check for the value and shares
            if not share_price:
                self.share_price = self.get_close_price(timestamp)
            else:
                self.share_price = share_price

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
        try:
            price = self.get_close_price(date)

            self.value = self.shares * price
            updated = True
        except IndexError:
            updated = False

        return updated

    def update_sector(self, sector):
        self.sector = sector

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


def convert_date(date_raw):
    periods = date_raw.split('/')

    year = str(periods[2])
    # reformat year
    if len(year) != 4:
        year = int(f"20{year[-2:]}")
    else:
        year = int(year)

    month = int(periods[0])
    day = int(periods[1])

    date = dt(year, month, day)

    return date
