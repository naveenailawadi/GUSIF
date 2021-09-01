from Risk.HistoricalReturnAnalysis import AnalyzedHolding, ReturnsDataHandler
import pandas as pd
import sys


# make a main function to handle everythin
def analyze(data_directory, output_file):
    # make a data handler to get all the tickers
    data_handler = ReturnsDataHandler(data_directory)

    tickers = data_handler.current_tickers()

    # create a list of analyzed holdings
    analyzed_holdings = []

    for ticker in tickers:
        print(f"Analyzing {ticker}")
        holding = AnalyzedHolding(f"{data_directory}/{ticker}.csv")

        holding_data = {
            "ticker": holding.ticker,
            "start_price": holding.start_price,
            "end_price": holding.end_price,
            "hpr": holding.hpr,
            "arithmetic_average_daily_return": holding.arithmetic_average_daily_return,
            "geometric_average_daily_return": holding.geometric_average_daily_return,
            "arithmetic_average_annualized_return": holding.arithmetic_average_annualized_return,
            "geometric_average_annualized_return": holding.geometric_average_annualized_return,
            "daily_return_stdev": holding.daily_return_stdev,
            "annualized_return_stdev": holding.annualized_return_stdev
        }

        # add the data to the analyzed holdings list
        analyzed_holdings.append(holding_data)

    # export the analysis
    df = pd.DataFrame(analyzed_holdings)
    df.to_excel(f"{output_file.split('.')[0]}.xlsx")


if __name__ == '__main__':
    # get the arguments from the system
    data_directory = sys.argv[1]
    output_file = sys.argv[2]

    # analyze the data
    analyze(data_directory, output_file)
