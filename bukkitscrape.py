import requests
from bs4 import BeautifulSoup
import  json
Spigot = 'https://getbukkit.org/download/spigot'
Bukkit = 'https://getbukkit.org/download/craftbukkit'
def requestVersionsBuckkit(buttonPressed):
        global downloads
        if buttonPressed == "Bukkit":
                downloads = gatherData(Bukkit)
                versions = [download.find(class_='col-sm-3').find("h2").getText() for download in downloads]
                return(versions)
        if buttonPressed == "Spigot":
                downloads = gatherData(Spigot)
                versions = [download.find(class_='col-sm-3').find("h2").getText() for download in downloads]
                print(versions)
                return(versions)

def requestDownloadBuckkit(selectedver):
        downloadlinks = [BeautifulSoup(requests.get(downloads[selectedver].find(class_='col-sm-4').find(class_='btn-group').find('a')['href']).content, 'html.parser').find("h2").find('a')['href']]
        return(downloadlinks)

def gatherData(webPage):
        page = requests.get(webPage)
        soup = BeautifulSoup(page.content, 'html.parser')
        downloads = soup.find(id='download')
        downloads = (downloads.find_all(class_='row vdivide'))
        return(downloads)

def requestVersionsPaper():
        page = requests.get('https://papermc.io/api/v1/paper')
        pagedict = json.loads(page.text)
        return(pagedict["versions"])