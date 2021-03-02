from Tracker import PriceMonitor
from datetime import datetime as dt
import sys

TICKERS = ['XLK', 'DELL', 'GOOG', 'LYFT', 'AVGO']


def parse_date(arg):
    # split the arg into month/day/year (because we live in the us)
    month, day, year = tuple([int(i) for i in arg.split('/')])

    # make a date object
    date = dt(year, month, day)

    return date


# make a main function
def main(start_date, end_date):
    # make a bunch of price monitors
    stocks = [PriceMonitor(t) for t in TICKERS]

    # find the returns based on the timeframes
    for stock in stocks:
        absolute_returns, percent_returns = stock.get_returns_on_timeframe(
            start_date, end_date)

        print(f"{stock.ticker}: {stock.format_change(percent_returns)}")


if __name__ == '__main__':
    # get the dates
    start_date = parse_date(sys.argv[1])
    end_date = parse_date(sys.argv[2])

    # call the main function
    main(start_date, end_date)
