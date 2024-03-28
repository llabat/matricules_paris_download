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
#from ipywidgets import FloatProgress
from selenium.webdriver.support.ui import Select
import math
import re
import sys

class TooManyResults(Exception):
    pass

class NoResults(Exception):
    pass

class DidntCatchThemAll(Exception):
    pass

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def merge_dfs(directorypath):
    dflist = []
    for filename in os.listdir(directorypath):
        try:
            df = pd.read_csv(directorypath+'/'+filename, index_col=0)
        except:
            print(filename)
        if len(df):
            dflist.append(df)
    return pd.concat(dflist)