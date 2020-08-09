from Tracker import PriceMonitor, suppress_stdout

if __name__ == '__main__':
    # list the tickers
    tickers = ['SPY', 'XLK', 'XLC', 'XLV', 'XLY',
               'XLE', 'XLU', 'XLB', 'XLI', 'MCHI', 'GLD']
    for ticker in tickers:
        with suppress_stdout():
            monitor = PriceMonitor(ticker)
            change = monitor.get_trading_weekly_change()

        print(f"{monitor.info['longName']} ({ticker}): {change}\n")
