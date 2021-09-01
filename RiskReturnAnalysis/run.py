from RiskReturnAnalysis.download_data import download
from RiskReturnAnalysis.analyze_tickers import analyze
import sys


def run(ticker_file, data_directory, output_file):
    # download
    download(ticker_file, data_directory)

    # analyze
    analyze(data_directory, output_file)


if __name__ == '__main__':
    # get the arguments from the system
    ticker_file = sys.argv[1]
    data_directory = sys.argv[2]
    output_file = sys.argv[3]

    # run everything
    run(ticker_file, data_directory, output_file)
