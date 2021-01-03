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
        self.qboxLayout()
        self.getFolder()

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
        self.selectClass.itemClicked.connect(self.TreeWidgetClicked)

        self.returnedItems = QtWidgets.QListWidget()
        self.Gridlayout.addWidget(self.returnedItems, 1, 0)
        self.returnedItems.itemClicked.connect(self.onReturnSelected)
        Widget.setLayout(self.Gridlayout)
    
    def TreeWidgetClicked(self, item):
        self.searchButton = QPushButton("Search")
        self.GridlayoutRightSide.addWidget(self.searchButton, 0, 0)
        self.searchButton.clicked.connect(self.search)
        self.selectedClassItem = item.text(0)
        if self.selectedClassItem == "Authors List":
            self.authorName = QLineEdit()
            self.GridlayoutRightSide.addWidget(self.authorName, 1, 0)

    def search(self):
        self.AuthorNameAndID = {}
        self.returnedItems.clear()
        if self.selectedClassItem == "Authors List":
            for key in Authors.AuthorSearch(searchtype=self.authorName.text()):
                self.returnedItems.addItem(key['name'])
                self.AuthorNameAndID[key["name"]] = key["id"]

    def onReturnSelected(self, item):
        self.ItemSelected = item.text()
        self.returnedItems.clear()
        if self.selectedClassItem == "Authors List":
            self.AuthorList()
            return

        if self.selectedClassItem == "Resources":
            self.ResourceSearch()
            return

        if self.selectedClassItem == "ResourceVersions":
            print("Here")
            self.ResourceVersions()
            return
        
        if self.selectedClassItem == "GetCfClearance":
            self.GetCfClearance()

    def AuthorList(self):
        self.ResourceIds = {}
        self.selectedClassItem = "ResourceVersions"
        for key in Authors.AuthorResources(author=self.AuthorNameAndID[self.ItemSelected]):
            self.returnedItems.addItem(key['name'])
            if key['name'] not in self.ResourceIds:
                self.ResourceIds[key['name']] = {}
                self.ResourceIds[key['name']] = [key['id']]
        print(self.ResourceIds)

    def ResourceSearch(self):
        for key in Resources.ResourceSearch(query=self.ItemSelected):
            pass
    
    def ResourceVersions(self):
        self.ResourceInfo = {}
        self.selectedClassItem = "GetCfClearance"
        for key in Resources.ResourceVersions(resource=self.ResourceIds[self.ItemSelected][0], size=1000):
            name = key['name']
            while name in self.ResourceInfo:
                name += '.0'
            self.returnedItems.addItem(name)
            self.ResourceInfo[name] = [key['id'], key['resource'], key['releaseDate']]
        print(self.ResourceInfo)

    def GetCfClearance(self):
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
        self.GetDownload(cf_clearance)
    
    def GetDownload(self, cf_clearance):
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': "cf_clearance="+cf_clearance
        }
        url = 'https://www.spigotmc.org/resources/'+str(self.ResourceInfo[self.ItemSelected][1])+'/download?version='+str(self.ResourceInfo[self.ItemSelected][0])
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
        fileName = self.fileSelected+'/plugins/'+str(self.ResourceInfo[self.ItemSelected][1])+'.'+str(self.ResourceInfo[self.ItemSelected][0])+'.'+str(self.ResourceInfo[self.ItemSelected][2])+ContentType
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
