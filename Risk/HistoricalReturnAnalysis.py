import requests

# create a folder where you will keep all the downloaded information
DOWNLOAD_FOLDER = "Risk/HistoricalReturns"

# make a returns analyzer class
class ReturnsAnalyzer:
    def __init__(self, output_file):
        # save the output file
        self.output_file = output_file

    # make a function to get the historical returns of one stock
    # period start and end are in seconds
    def get_daily_returns(self, ticker, period_start, period_end, download_folder=DOWNLOAD_FOLDER):
        # make the url
        url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period_start}&period2={period_end}&interval=1d&events=history&includeAdjustedClose=true"

        # make an outfile
        outfile = f"{download_folder}/{ticker}"

        # request the data from the url -> download it into csv
        with open(, 'wb') as f, \
                requests.get(url, stream=True) as r:
            for line in r.iter_lines():
                f.write(line+'\n'.encode())

'''
NOTES
- sample URL for csv download
https://query1.finance.yahoo.com/v7/finance/download/NFLX?period1=1609459200&period2=1630368000&interval=1d&events=history&includeAdjustedClose=true
'''
