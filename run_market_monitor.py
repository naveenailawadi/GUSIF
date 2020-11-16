from MarketMonitor import ForexMonitor, CommodityMonitor, BondMonitor
from MarketMonitor.secrets import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from MarketMonitor.TelegramBot import Messenger
from Tracker import PriceMonitor, suppress_stdout
from forex_python.bitcoin import BtcConverter
from datetime import datetime as dt
import schedule
import time


# create the classes as constants
MESSENGER = Messenger(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
FOREX_MONITOR = ForexMonitor()
COMMODITY_MONITOR = CommodityMonitor()
BOND_MONITOR = BondMonitor()
BITCOIN_MONITOR = BtcConverter()

# create lists of the symbols
FOREX_SYMBOLS = ['EUR', 'CNY']
BOND_YEARS = [10, 30]
RATES_SEND_TIME = '09:00'
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
RATES_HTML = 'MarketMonitor/templates/rates.html'

# sector settings
SECTORS = ['SPY', 'XLK', 'XLC', 'XLV',
           'XLY', 'XLF', 'XLE', 'XLU', 'XLB', 'XLI']
SECTORS_SEND_TIME = '16:30'
SECTORS_HTML = 'MarketMonitor/templates/sectors.html'


def get_date():
    # get the current date
    today = dt.now()
    date = f"{today.month}/{today.day}/{today.year} ({today.hour}:{str(today.minute).zfill(2)})"

    return date


# create a function that gets all the prices and sends them
def send_rates():
    date = get_date()

    # get the current forex prices
    forex_rates = [FOREX_MONITOR.usd_to(symbol) for symbol in FOREX_SYMBOLS]

    # get the commodity prices
    oil_price = COMMODITY_MONITOR.get_wti_price()
    gold_price = COMMODITY_MONITOR.get_gold_price()
    btc_price = f"Bitcoin: ${format(round(BITCOIN_MONITOR.get_latest_price('USD'),2), ',')}"

    # get the 10 year and 30 year bond prices
    bond_rates = [(year, BOND_MONITOR.get_yield(year)) for year in BOND_YEARS]

    information = {
        'date': date,
        'forex_rates': forex_rates,
        'commodities': [oil_price, gold_price, btc_price],
        'bond_rates': bond_rates
    }

    # send it with telegram
    MESSENGER.send_html(information, RATES_HTML)


def check_sectors():
    sector_info = []
    date = get_date()
    for ticker in SECTORS:
        with suppress_stdout():
            monitor = PriceMonitor(ticker)
            change = monitor.get_trading_weekly_change()
        info = {
            'ticker': monitor.ticker,
            'name': monitor.info['longName'],
            'change': change
        }
        sector_info.append(info)

    # render some html to send
    information = {
        'date': date,
        'sectors': sector_info
    }

    MESSENGER.send_html(information, SECTORS_HTML)


# send it over and over on a schedule
if __name__ == '__main__':
    for name in DAYS:
        statement = f"schedule.every().{name}.at(RATES_SEND_TIME).do(send_rates)"
        exec(statement)
        print(f"Added {name}")

    # add the sector one
    schedule.every().friday.at(SECTORS_SEND_TIME).do(check_sectors)
    print('Added sector monitor')

    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(10)
    '''
    send()
    '''
