from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os,sys
import csv
import time

#DATA = "table.txt"
DATA = "berenices.txt"
download_path = "/mnt/6708B5D108FCE57A/Downloads/"+ "galaxies/"

with open(DATA) as f:
    lines = f.readlines()
    f.close()
#For each line in the data file
coords = [["Name", "RA", "DEC"]]
for line in lines:
    #data grooming
    line = line.strip()
    column = line.split()
    if column != [] and "NGC" not in column:

        url = f"http://archive.stsci.edu/cgi-bin/dss_form?target=NGC+{column[0]}&resolver=SIMBAD"
        #Some browser options required to download files unattended
        options = Options() 
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.dir", download_path)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/x-fits")
        options.headless = True #Set to false if needed to actually see steps being performed
        driver = webdriver.Firefox(options=options,firefox_profile=fp)
        #Go to target url and simulate button presses and keystrokes
        driver.get(url)
        driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/select/option[5]").click()
        ra = driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/p[1]/input[1]").get_attribute('value')
        dec = driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/p[1]/input[2]").get_attribute('value')
        driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/p[2]/input[1]").clear()
        driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/p[2]/input[1]").send_keys('10.0')     
        driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/p[2]/input[2]").clear()
        driver.find_element_by_xpath("/html/body/b/form[2]/center[1]/p[2]/input[2]").send_keys('10.0')
        driver.find_element_by_xpath("/html/body/b/form[2]/center[2]/input[1]").click()
        #Wait for download to finish
        while True:
            if not os.path.exists(download_path+"dss_search.part") and os.path.exists(download_path+"dss_search"):
                time.sleep(3)
                break
        #Rename file accordingly and populate coordinates list
        os.rename(download_path+"dss_search",download_path+f"NGC{column[0]}")
        coords.append([f"NGC{column[0]}",ra,dec])
        print(f"Done NGC {column[0]}")
        driver.quit()

with open("coords.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(coords)