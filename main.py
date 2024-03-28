import os
import pandas as pd
from crawling import Downloading_Spider
from threads import Parallel_Downloader

import argparse

# Default values for the constants
DEFAULT_DRIVERPATH = '/Users/leolabat/Downloads/chromedriver-mac-arm64-2/chromedriver'
DEFAULT_WORKERDIR = '/Users/leolabat/Desktop/'
DEFAULT_OUTPUTDIR = '/Users/leolabat/Desktop/tirage/'
DEFAULT_CSV_FILE = "/Users/leolabat/Downloads/tirage_paris.csv"

# Set up the argument parser
parser = argparse.ArgumentParser(description='My Program Description')

# Add arguments
parser.add_argument('--driverpath', type=str, default=DEFAULT_DRIVERPATH,
                    help='Path to the Chrome driver')
parser.add_argument('--workdir', type=str, default=DEFAULT_WORKERDIR,
                    help='Working directory path')
parser.add_argument('--outputdir', type=str, default=DEFAULT_OUTPUTDIR,
                    help='Output directory path')
parser.add_argument('--csvpath', type=str, default=DEFAULT_CSV_FILE,
                    help='CSV file path')

# Parse arguments
args = parser.parse_args()

# Overwrite constants if arguments are provided
DRIVERPATH = args.driverpath
WORKERDIR = args.workdir
OUTPUTDIR = args.outputdir
CSVFILE = args.csvpath

if not os.path.exists(OUTPUTDIR):
    # If it does not exist, create it
    os.makedirs(OUTPUTDIR)
    print(f"Directory '{OUTPUTDIR}' was created.")
else:
    # If it exists, print a message
    print(f"Directory '{OUTPUTDIR}' already exists.")

df = pd.read_csv(CSVFILE)

spiders = Parallel_Downloader(DRIVERPATH, WORKERDIR, OUTPUTDIR, 10, df[:100])

#spider = Downloading_Spider(DRIVERPATH, WORKERDIR, OUTPUTDIR, df[:5])