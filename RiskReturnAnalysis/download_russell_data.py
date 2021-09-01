from Risk.HistoricalReturnAnalysis import ReturnsDataHandler
import pandas as pd
import time

# set the ticker data
TICKER_FILE = 'RiskReturnAnalysis/Russell2000_8_31.csv'


# download all the data with the Returns handler
def main():
    # make an handler
    handler = ReturnsDataHandler()

    # import all the tickers
    tickers = list(pd.read_csv(TICKER_FILE)['tickers'])

    # find the current data
    found_tickers = handler.current_tickers()

    # remove the foudn tickers from the tickers list
    tickers = [ticker for ticker in tickers if ticker not in found_tickers]

    print(f"Looking for {len(tickers)} tickers")

    # run the handler for all the tickers
    for ticker in tickers:
        handler.get_daily_returns(ticker, 1609459200, 1630368000)
        time.sleep(1)


if __name__ == '__main__':
    main()
