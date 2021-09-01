from Risk.HistoricalReturnAnalysis import ReturnsDataHandler
import pandas as pd
import time
import sys


# download all the data with the Returns handler
def download(ticker_file, output_directory, column_header='tickers'):
    # make an handler
    handler = ReturnsDataHandler(output_directory)

    # import all the tickers
    tickers = list(pd.read_csv(ticker_file)[column_header])

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
    # get the arguments from the system
    ticker_file = sys.argv[1]
    output_directory = sys.argv[2]

    # download the data
    download(ticker_file, output_directory)
