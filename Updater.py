import os
import json
from library import Resources
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
def checkForUpdate():
    with open('selectedFile.json') as r:
        temp = json.load(r)
        fileSelected = temp['File']
    for item in os.listdir(fileSelected+'/plugins/'):
        if '.jar' or '.zip' in item:
            ResourceID = item.split('.')[0]
            ResourceDate = item.split('.')[2]
            for key in Resources.ResourceVersions(ResourceID, size=1000, sort="+releaseDate"):
                if key['releaseDate'] > int(ResourceDate):
                    ResourceDate = key['releaseDate']
                if ResourceDate == key['releaseDate']:
                    DownloadInfo = [key['resource'], key['id'], key['releaseDate']]
                    return(DownloadInfo)
def GetCfClearance():
    PATH = 'C:/Users/Haydomon/Documents/chromedriver.exe'
    url = 'https://spigotmc.org/'
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options, executable_path=PATH)
    driver.execute_script(f"window.open('{url}')")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    while True:
        try:
            cf_clearance = driver.get_cookie("cf_clearance")["value"]
            break
        except TypeError:
            time.sleep(0.1)
    driver.close()
    return(cf_clearance)
def GetDownload():
    DownloadInfo = checkForUpdate()
    cf_clearance = GetCfClearance()
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'cookie': "cf_clearance="+cf_clearance
    }
    url = 'https://www.spigotmc.org/resources/'+str(DownloadInfo[0])+'/download?version='+str(DownloadInfo[1])
    r = requests.get(url, headers=headers)
    try:
        r.headers['Content-Disposition']
    except KeyError:
        print("Returned")
        return
    if ".jar" in r.headers['Content-Disposition']:
        ContentType = '.jar'
    else:
        ContentType = '.zip'
    print(DownloadInfo)
    fileName = 'C:/Users/Haydomon/Documents/Test Server'+'/plugins/'+str(DownloadInfo[0])+'.'+str(DownloadInfo[1])+'.'+str(DownloadInfo[2])+ContentType
    with open(f'{fileName}', 'wb') as f:
        f.write(r.content)
GetDownload()