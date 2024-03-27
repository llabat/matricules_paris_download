import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import os
import pandas as pd
import numpy as np
import shutil
import tqdm
import random
from concurrent.futures import ThreadPoolExecutor
from ipywidgets import FloatProgress
from selenium.webdriver.support.ui import Select
import math
import re
import sys

from utils import divide_chunks
from crawling import Downloading_Spider, LittleSpider

class Parallel_Downloader():
    
    def __init__(self, DRIVERPATH, WORKERDIR, OUTPUTDIR, nworkers, df):
        
        self.start_time = time.time()
        self.nworkers = nworkers
        self.files = list(divide_chunks(df.sample(frac=1),int(len(df)/self.nworkers)))
        self.failed = []
        
        self.spider_coffin = []

        self.DRIVERPATH = DRIVERPATH
        self.WORKERDIR = WORKERDIR
        self.OUTPUTDIR = OUTPUTDIR

        self.main()
        
    def main(self):
        
        with ThreadPoolExecutor(max_workers=self.nworkers) as executor:
            self.spider_coffin = executor.map(lambda file_chunk: Downloading_Spider(self.DRIVERPATH, self.WORKERDIR, self.OUTPUTDIR, file_chunk), self.files)
        
        for deads in self.spider_coffin:
            self.failed += deads.failed        
        
        print(f'{len(self.failed)} records not obtained.')
        print(f'{len(self.files[0])*self.nworkers - len(self.failed)} records were processed in {round((time.time() - self.start_time))} seconds.')


class Little_Parallelizer():
    
    def __init__(self, nworkers, df):
        
        self.start_time = time.time()
        self.nworkers = nworkers
        self.files = list(divide_chunks(df.sample(frac=1),int(len(df)/self.nworkers)))
        
        self.spider_coffin = []

        self.main()
        
    def main(self):
        
        with ThreadPoolExecutor(max_workers=self.nworkers) as executor:
            self.spider_coffin = executor.map(LittleSpider, self.files)
        
        nb_records = 0
        for spider in self.spider_coffin:
            nb_records += len(spider.data)

        #print(f'{len(self.failed)} records not obtained.')
        print(f'{nb_records} records were processed in {round((time.time() - self.start_time))} seconds.')
