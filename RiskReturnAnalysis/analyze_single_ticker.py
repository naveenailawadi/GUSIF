from Risk.HistoricalReturnAnalysis import AnalyzedHolding
import sys


# make a main function to handle everythin
def main(ticker):
    holding = AnalyzedHolding(f"Risk/HistoricalReturns/{ticker}.csv")

    print(f"HPR: {holding.hpr}")
    print(f"Arith Daily Avg: {holding.arithmetic_average_daily_return}")
    print(f"Geom Daily Avg: {holding.geometric_average_daily_return}")
    print(
        f"Arith Avg Annualized: {holding.arithmetic_average_annualized_return}")
    print(
        f"Geom Avg Annualized: {holding.geometric_average_annualized_return}")
    print(f"Daily Return stdev: {holding.daily_return_stdev}")
    print(f"Annualized Return stdev: {holding.annualized_return_stdev}")


if __name__ == '__main__':
    ticker = sys.argv[1]
    main(ticker)
