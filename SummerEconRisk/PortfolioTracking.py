from EarningsCalculator import TimeFrame
from Tracker import Holding
from Scraping import PorfolioScraper
from secrets import BIVIO_USERNAME, BIVIO_PASSWORD
from datetime import datetime as dt
import pandas as pd
import numpy as np


class Portfolio:
    def __init__(self, name, holdings=[]):
        self.holdings = holdings
        self.name = name

    def add_holding(self, ticker, value=None, shares=None, timestamp=dt.now()):
        new_holding = Holding(ticker, value, shares, timestamp)

        self.holdings.append(new_holding)

    def total_value(self):
        total_value = np.nansum(np.asarray(
            [holding.value for holding in self.holdings]).astype(float))

        return total_value

    # create a function that returns the holding and it's value as a tuple
    def portfolio_proportion(self, ticker):
        tickers = [holding.ticker for holding in self.holdings]

        index = tickers.index(ticker)

        proportion = self.holdings[index].set_proportion(self.total_value())

        return proportion

    def make_current(self):
        for holding in self.holdings:
            holding.update_value()

    def __repr__(self):
        return f"{self.name} - {[holding.ticker for holding in self.holdings]}"


# make a class to handle all holdings data
class HoldingsManager(TimeFrame):
    def __init__(self, holdings_df, sector_df):
        self.holdings_data = holdings_df
        self.sector_data = sector_df

        self.sectors = self.sector_data.columns
        self.tickers = sum([list(self.sector_data[sector])
                            for sector in self.sectors], [])

        holding_tickers = [column.split(' ')[0].strip()
                           for column in self.holdings_data]
        self.holdings_data.columns = holding_tickers

    # create a function that gets all the current holdings
    def get_holdings(self, date, tickers=None):
        current_values = self.holdings_data.tail(1)

        # make a holding for every ticker in the tickers
        holdings = [self.create_holding(
            ticker, current_values, date) for ticker in tickers]
        holdings = [holding for holding in holdings if holding]

        return holdings

    # match the current holdings to the sector
    def get_sector_portfolios(self, date=None, holdings=None, holdings_dict=None):
        portfolios = []
        # match a sector name with the tickers in it
        portfolio_lists = [(sector, list(self.sector_data[sector]))
                           for sector in self.sectors]

        for sector, portfolio in portfolio_lists:
            if not holdings:
                holdings = self.get_holdings(date, tickers=portfolio)
            else:
                holdings = [holdings_dict[ticker]
                            for ticker in portfolio if not pd.isnull(ticker)]

            new_portfolio = Portfolio(sector, holdings)
            portfolios.append(new_portfolio)

        return portfolios

    # make a handled way to make a holding

    def create_holding(self, ticker=[], current_values=[], date=None, holding=None):
        if not holding:
            if ticker in current_values.columns:
                value = list(current_values[ticker])[0]
                if not value:
                    return None
                holding = Holding(ticker, value=value,
                                  timestamp=date)
            else:
                holding = None
                print(f"No holding data found for {ticker}")

        return holding


if __name__ == '__main__':
    # load in the holdings
    sectors_df = pd.read_csv('SummerEconRisk/Private/holdings.csv')

    # get the holdings from a scraper
    scraper = PorfolioScraper(headless=True)
    scraper.login(BIVIO_USERNAME, BIVIO_PASSWORD)
    holdings, date = scraper.scrape_holdings()
    scraper.quit()
    holdings_df_loading = {
        holding.ticker: holding.shares for holding in holdings}
    holdings_df = pd.DataFrame(
        holdings_df_loading, index=list(range(len(holdings))))

    manager = HoldingsManager(holdings_df, sectors_df)

    holdings_dict = {holding.ticker: holding for holding in holdings}
    portfolios = manager.get_sector_portfolios(
        holdings=holdings, holdings_dict=holdings_dict)

    # export the portfolio data to some folder
    portfolio_values = np.asarray(
        [portfolio.total_value() for portfolio in portfolios]).astype(float)
    total_fund_value = np.nansum(portfolio_values)
    sector_weighting_dict = {
        'Sector': [portfolio.name for portfolio in portfolios],
        'Value': portfolio_values,
        'Proportion of Fund': portfolio_values / total_fund_value
    }
    sector_export_df = pd.DataFrame(sector_weighting_dict)
    sector_export_df.to_csv(
        f"SummerEconRisk/Private/Sector Weight ({date.month}-{date.day}-{date.year}).csv", index=False)

    # analyze each stock individually

    # make a holding name list
    holding_names = sum([[holding.ticker for holding in portfolio.holdings]
                         for portfolio in portfolios], [])

    # make a portfolio name list
    portfolio_names = sum(
        [[portfolio.name for holding in portfolio.holdings] for portfolio in portfolios], [])

    # get the holding values and shares
    holding_values = np.asarray(sum(
        [[holding.value for holding in portfolio.holdings] for portfolio in portfolios], [])).astype(float)
    holding_shares = np.asarray(sum(
        [[holding.shares for holding in portfolio.holdings] for portfolio in portfolios], [])).astype(float)
    portfolio_holding_values = np.asarray(sum([[portfolio.total_value(
    ) for holding in portfolio.holdings] for portfolio in portfolios], [])).astype(float)

    # get the proportion of the sector
    holding_sector_proportions = holding_values / portfolio_holding_values

    # get the stock as a proportion of the fund
    holding_fund_proportions = holding_values / total_fund_value

    # export the data to a dataframe
    holding_weighting_dict = {
        'Stock': holding_names,
        'Sector': portfolio_names,
        'Value': holding_values,
        'Shares': holding_shares,
        'Sector Proportion': holding_sector_proportions,
        'Fund Proportion': holding_fund_proportions
    }

    holding_weight_df = pd.DataFrame(holding_weighting_dict)
    holding_weight_df.to_csv(
        f"SummerEconRisk/Private/Holdings Weight ({date.month}-{date.day}-{date.year}).csv", index=False)
