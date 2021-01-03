from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from directoryInfo import *
from library import Authors, Resources
import requests
import sys
import qdarkstyle
import bukkitscrape
from selenium import webdriver
import subprocess
import os
import json
import math
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
selectedver = None
selectedversiontxt = None
class serverGeneration(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Klem"
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initWindow()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("tree.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.getFolder()
        serverGeneration.qboxLayout(self)

    def qboxLayout(self):
        Widget = QtWidgets.QWidget(self)
        self.setCentralWidget(Widget)

        self.Gridlayout = QtWidgets.QGridLayout()
        self.GridlayoutRightSide = QtWidgets.QGridLayout()
        self.Gridlayout.addLayout(self.GridlayoutRightSide, 0, 1)
        self.spacer = QSpacerItem(0,100, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.GridlayoutRightSide.addItem(self.spacer, 4, 0)
        self.selectClass = QTreeWidget()
        self.selectClass.setHeaderLabel('Categories')
        self.selectClass.setAlternatingRowColors(True)
        self.Author = QtWidgets.QTreeWidgetItem(self.selectClass, ['Author'])
        self.AuthorC1 = QtWidgets.QTreeWidgetItem(self.Author, ['Authors List'])
        self.AuthorC2 = QtWidgets.QTreeWidgetItem(self.Author, ['Author Details'])
        self.AuthorC3 = QtWidgets.QTreeWidgetItem(self.Author, ['Author Resources'])
        self.AuthorC4 = QtWidgets.QTreeWidgetItem(self.Author, ['Author Reviews'])
        self.Resources = QtWidgets.QTreeWidgetItem(self.selectClass, ['Resources'])
        self.ResourcesC1 = QtWidgets.QTreeWidgetItem(self.Resources, ['Resources'])
        self.ResourcesC2 = QtWidgets.QTreeWidgetItem(self.Resources, ['Resource for Version'])
        self.ResourcesC3 = QtWidgets.QTreeWidgetItem(self.Resources, ['Free Resources'])
        self.ResourcesC4 = QtWidgets.QTreeWidgetItem(self.Resources, ['New Resources'])
        self.ResourcesC5 = QtWidgets.QTreeWidgetItem(self.Resources, ['Premium Resources'])
        self.ResourcesC6 = QtWidgets.QTreeWidgetItem(self.Resources, ['Search Resource'])
        self.Gridlayout.addWidget(self.selectClass, 0, 0)
        self.selectClass.itemClicked.connect(self.onItemClicked)

        self.returnedItems = QtWidgets.QListWidget()
        self.Gridlayout.addWidget(self.returnedItems, 1, 0)
        self.returnedItems.itemClicked.connect(self.onReturnSelected)
        Widget.setLayout(self.Gridlayout)

    def onItemClicked(self, item):
        self.SelectedCategory = item.text(0)
        if "Author" in item.text(0):
            self.authorName = QLineEdit()
            self.GridlayoutRightSide.addWidget(self.authorName, 1, 0)
        self.sortType = QComboBox()
        self.sortType.addItem("+releaseDate")
        self.sortType.addItem("-releaseDate")
        self.GridlayoutRightSide.addWidget(self.sortType, 2, 0)
        self.searchButton = QPushButton("Search")
        self.GridlayoutRightSide.addWidget(self.searchButton, 0, 0)
        self.searchButton.clicked.connect(lambda: self.search(item))

    def search(self, item):
        self.SelectedCategory = item.text(0)
        self.NamesIdDict = {}
        self.returnedItems.clear()
        if item == False:
            print("Fail Search")
        if item.text(0) == "Authors List":
            for key in Authors.AuthorSearch(searchtype=self.authorName.text()):
                self.returnedItems.addItem(key["name"])
                self.NamesIdDict[key["name"]] = key["id"]
                
    def onReturnSelected(self, item):
        Selected = item.text()
        self.ResourceIds = {}
        self.returnedItems.clear()
        if self.SelectedCategory == "Authors List":
            self.SelectedCategory = "AuthorsPlugins"
            for key in Authors.AuthorResources(author=self.NamesIdDict[Selected]):
                self.returnedItems.addItem(key["name"])
                print(self.SelectedCategory)
            return
            
        if self.SelectedCategory == "AuthorsPlugins":
            self.SelectedCategory = "ResourceVersions"
            for key in Resources.ResourceSearch(query=Selected):
                if 'resourceID' not in self.ResourceIds:
                    self.ResourceIds['resourceID'] = {}
                    self.ResourceInfo = {}
                    self.ResourceInfo['resourceID'] = {}
                if key['name'] == Selected:
                    self.ResourceIds['resourceID'][key['id']] = []
                print(self.ResourceIds)

        if self.SelectedCategory == "ResourceVersions":
            if 'resourceID' in self.ResourceIds:
                for i in self.ResourceIds['resourceID']:
                    self.SelectedCategory = "ResourceVersionDownload"
                    for key in Resources.ResourceVersions(resource=i, size=1000, sort=str(self.sortType.currentText())):
                        if key["resource"] == i:
                            if key['name'] in self.ResourceInfo['resourceID']:
                                self.ResourceInfo['resourceID'][key['name']+".0"] = []
                                self.ResourceInfo['resourceID'][key['name']+".0"].append(key["id"])
                                self.ResourceInfo['resourceID'][key['name']+".0"].append(key["resource"])
                                self.ResourceInfo['resourceID'][key['name']+".0"].append(key["releaseDate"])
                                self.returnedItems.addItem(key["name"]+".0")
                            else:
                                self.ResourceInfo['resourceID'][key['name']] = []
                                self.ResourceInfo['resourceID'][key['name']].append(key["id"])
                                self.ResourceInfo['resourceID'][key['name']].append(key["resource"])
                                self.ResourceInfo['resourceID'][key['name']].append(key["releaseDate"])
                                self.returnedItems.addItem(key["name"])
                    print(self.ResourceInfo)
                return
        if self.SelectedCategory == "ResourceVersionDownload":
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
            self.SelectedCategory = "GetDownlaod"

        if self.SelectedCategory == "GetDownlaod":
            print("Here")
            headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
            'cookie': "cf_clearance="+cf_clearance
            }
            url = 'https://www.spigotmc.org/resources/'+str(self.ResourceInfo['resourceID'][Selected][1])+'/download?version='+str(self.ResourceInfo['resourceID'][Selected][0])
            r = requests.get(url, headers=headers)
            if ".jar" in r.headers['Content-Disposition']:
                ContentType = '.jar'
            else:
                ContentType = '.zip'
            fileName = self.fileSelected+'/plugins/'+str(self.ResourceInfo['resourceID'][Selected][1])+'.'+str(self.ResourceInfo['resourceID'][Selected][0])+'.'+str(self.ResourceInfo['resourceID'][Selected][2])+ContentType
            with open(f'{fileName}', 'wb') as f:
                f.write(r.content)
        
    def getFolder(self):
        with open('selectedFile.json') as r:
            temp = json.load(r)
            self.fileSelected = temp['File']

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = serverGeneration()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window.show()
    sys.exit(app.exec())
