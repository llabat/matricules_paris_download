import re
import os
import time
import random
import shutil
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException


from const import DRIVERPATH, WORKERDIR, OUTPUTDIR
from utils import DidntCatchThemAll

class Downloading_Spider():
    
    def __init__(self, DRIVERPATH, WORKERDIR, OUTPUTDIR, df):
        
        self.df = df
        self.prev_url = ''
        self.failed = []
        self.matricule_table = []
        self.name = 'worker' + str(random.randint(0,100000000))
        
        self.current_ntotal = None
        
        self.workerdir = WORKERDIR + self.name
        os.mkdir(self.workerdir)
        
        options = webdriver.ChromeOptions()
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.workerdir}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless")  # Enable headless mode
        options.add_argument("--disable-gpu")  # Optional, but recommended
        options.add_argument("--no-sandbox")  # Bypass OS security model, OPTIONAL
        options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems, OPTIONAL
        self.driver = webdriver.Chrome(executable_path=DRIVERPATH, chrome_options=options)
        
        self.main()
        
    def click_and_download(self):
        
        try :
            self.driver.find_element("id","arkoVision_next").click()
            time.sleep(2)
            self.driver.find_element("css selector","#input_uielem_download").click()
            time.sleep(3)
        except: 
            pass
        
    def download_all(self, n_total):
        
        for _ in range(n_total - 1):
            self.click_and_download()
        
        '''self.prev_url = self.driver.current_url
        self.click_and_download()
        
        while self.prev_url != self.driver.current_url :
            self.prev_url = self.driver.current_url
            self.click_and_download()'''
    
    def collect_all(self, link, rowid):
        
        self.driver.get(link)
        try :
            n_total = int(self.driver.find_element("id","nb_total").text)
        except : n_total = 1
        self.current_ntotal = n_total
        self.driver.find_element("css selector","#input_uielem_download").click()
        time.sleep(3)
        self.download_all(n_total)
        
        n_downloads = int(len([filename for filename in os.listdir(self.workerdir) if filename.endswith(".jpg")]))
        maxtime = 120
        while n_total != n_downloads :
            maxtime -= 3
            time.sleep(3)
            n_downloads = int(len([filename for filename in os.listdir(self.workerdir) if filename.endswith(".jpg")]))
            if maxtime == 0:
                break

        if n_total != n_downloads:
            print(f"{rowid} : not all scans collected.")
            raise DidntCatchThemAll
        else : print(f"{rowid} all scans collected.")
    
    def abort(self):
        for filename in os.listdir(self.workerdir):
            if filename.endswith(".jpg"):
                os.remove(filename)
        
    def main(self):
        for index, row in self.df.iterrows():
            fichedir =  OUTPUTDIR + str(row["labat_id"])
            os.mkdir(fichedir)
            try : self.collect_all(row["Lien"],row["labat_id"])     
            except DidntCatchThemAll :
                self.failed.append(row["labat_id"])
                self.abort()
                continue
            try:
                title = self.driver.find_element("css selector",".titre")
                dlist = re.findall("\d+",title.text)
            except:
                dlist = [None]
            self.matricule_table.append([row["labat_id"],dlist[0],self.current_ntotal])
            for filename in os.listdir(self.workerdir):
                if filename.endswith(".jpg"):
                    shutil.move(self.workerdir + "/" + filename, fichedir + "/" + filename)
        #pd.DataFrame(self.matricule_table,columns=["id","matricule","n_scans"]).to_csv('/Volumes/SAFE/tirage/worker_info/'+self.name+"_info.csv")
        shutil.rmtree(self.workerdir)
        self.driver.quit()


class LittleSpider():
    
    def __init__(self,df):
        
        self.data = []
        self.df = df
        self.name = 'worker' + str(random.randint(0,100000000))
        self.workerdir = WORKERDIR + self.name
        os.mkdir(self.workerdir)
        
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.workerdir}
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(DRIVERPATH, chrome_options = options)
        
        self.main()
    
    def main(self):
        
        for row in self.df.iterrows():
            self.driver.get(row[1]["Lien"])
            try:
                title = self.driver.find_element("css selector",".titre")
                dlist = re.findall("\d+",title.text)
                if dlist == []:
                    dlist = [None]
            except:
                dlist = [None]
            try :
                n_total = int(self.driver.find_element("id","nb_total").text)
            except : 
                n_total = 1

            self.data.append([row[1]["id"],dlist[0],n_total])
        final_table = pd.DataFrame(self.data)
        final_table.to_csv("/Users/leolabat/Desktop/matricules_numbers/"+self.name+".csv")

