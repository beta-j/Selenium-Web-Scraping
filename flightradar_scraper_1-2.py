# TITLE     FLIGHTRADAR24 STATISTICS SCRAPER
# VERSION   1.2
# DATE      04-DEC-2023
# AUTHOR    JAMES BALDACCHINO

## If you are using this with PowerBI - set it to look for a .csv file with the filename specified in dest_filename at the location specified by dest_directory

import glob
import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.chrome
from selenium.webdriver.chrome.options import Options
import time

dest_directory = "C:\\temp"                 # destination download directory
dest_filename = "f_flights.csv"             # destination filename
old_files = glob.glob(dest_directory+"\\" + '*.csv')
print("Existing Files in", dest_directory,": ",old_files)

#######Set some general options for Chrome to establish the download directory etc.. #########
chrome_options = webdriver.ChromeOptions()
prefs = {"download.default_directory" : dest_directory,
        "download.prompt_for_download":False,
        "download.directory_upgrade":True,
         "safebrowsing.enabled":False}
chrome_options.add_experimental_option("prefs",prefs)

##################################################################################

driver=webdriver.Chrome(options=chrome_options)         #use chrome as driver
url = "https://www.flightradar24.com/data/statistics"   #URL to be scraped
driver.get(url)                                         #open the URL
driver.maximize_window()

#################################################################################

try:                #check for consent button and click it if available
    consent_button = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']")))
    consent_button.click()
except Exception as e:
    print("Consent button not found or cookies already accepted")
time.sleep(5)

try:        #wait until the dark overlay on the screen disappears
    wait = WebDriverWait(driver,30)
    wait.until(EC.invisibility_of_element((By.XPATH, "//div[@class='onetrust-pc-dark-filter ot-fade-in']")))
except Exception as e:
    print("onetrust-pc-dark-filter not found")


try:    #locate and click on the burger button
    burger_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "(//*[@d='M 6 6.5 L 20 6.5 M 6 11.5 L 20 11.5 M 6 16.5 L 20 16.5'])[1]")))
    burger_button.click()
except Exception as e:
    print("Couldn't locate burger button")

try:    #locate and click on an entry in the dropdown that contains 'CSV'
    csv_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='highcharts-menu-item'][contains(.,'CSV')]")))
    csv_button.click()
except Exception as e:
    print("Couldn't locate download CSV element in drop down menu")




###################################################################     THIS SECTION RENAMES THE LAST DOWNLOADED FILE, SO FILENAME IS ALWAYS CONSISTENT

full_path = dest_directory+"\\"+dest_filename
files = glob.glob(dest_directory+"\\" + '*.csv')                                    # check the destination directory for CSV files
while files == old_files:
    files = glob.glob(dest_directory + "\\" + '*.csv')                              # check the destination directory for CSV files
    time.sleep(1)


latest_file = max(files, key=os.path.getctime)                                      # determine which file was created last
if os.path.exists(full_path):                                                       # check if a file with the same name already exists
    os.remove(full_path)                                                            # if it does, delete the file
    print("Deleted pre-existing file:", full_path)
print ("Renaming ",latest_file," to ", dest_filename, " in ", dest_directory)
os.rename(latest_file,full_path)                                                    # rename the file to the filename specified in dest_filename

## If you are using this with PowerBI - set it to look for a .csv file with the filename specified in dest_filename at the location specified by dest_directory
