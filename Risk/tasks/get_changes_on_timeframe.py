from Tracker import convert_date
from Risk.PortfolioTracking import make_portfolios
import pandas as pd
import os

MAX_PROCESSES = os.cpu_count()


def create_holding_data(holding, start_date, end_date):
    point_return, percent_returns = holding.get_returns_on_timeframe(
        start_date, end_date)

    # set the holding to the end date
    updated = holding.update_value(end_date)

    if updated:
        start_value = holding.value / (1 + percent_returns)
        end_value = holding.value
    else:
        start_value = None
        end_value = None

    # add aboslute return if possible
    if point_return:
        absolute_returns = holding.shares * point_return
    else:
        absolute_returns = None

    holding_data = {
        'Ticker': holding.ticker,
        'Sector': holding.sector,
        'Return Value per Share': point_return,
        'Percent Return': percent_returns,
        'Shares': holding.shares,
        f"Theoretical Value {start_date.month}-{start_date.day}-{start_date.year}": start_value,
        f"Theoretical Value {end_date.month}-{end_date.day}-{end_date.year}": end_value,
        'Absolute Return': absolute_returns
    }

    return holding_data


if __name__ == '__main__':
    '''
    sector_csv = input('Sector CSV: ').strip().replace('\\', '')

    # get the start and end date (month/day/year)
    start_date = convert_date(input('Start Date (mm/dd/yyyy): '))
    end_date = convert_date(input('End Date (mm/dd/yyyy): '))
    '''
    sector_csv = 'Risk/Private/holdings.csv'
    start_date = convert_date('02/12/2020')
    end_date = convert_date('08/07/2020')

    # create an export csv name
    export_csv = f"{os.path.dirname(sector_csv)}/Holdings Change ({start_date.month}-{start_date.day}-{start_date.year} to {end_date.month}-{end_date.day}-{end_date.year}).csv"

    sector_df = pd.read_csv(sector_csv)

    # create the portfolios
    portfolios, date = make_portfolios(sector_csv)

    holdings = sum([portfolio.holdings for portfolio in portfolios], [])

    # create a csv with holdings returns over a timeframe
    holdings_data = [create_holding_data(
        holding, start_date, end_date) for holding in holdings]

    # create and export the csv
    export_df = pd.DataFrame(holdings_data)
    export_df.to_csv(export_csv, index=False)
