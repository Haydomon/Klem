from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from directoryInfo import *
import sys
import qdarkstyle
import bukkitscrape
import wget
import urllib
import subprocess
import os
import json
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
        serverGeneration.menuSetup(self)
        serverGeneration.qboxLayout(self)
        serverGeneration.initalFolder(self)
        
    def menuSetup(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(serverGeneration.openAction(self))

    def openAction(self):
        openAction = QAction(QIcon('open.png'), '&Open     ', self)
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.fileSystem)
        return (openAction)

    def qboxLayout(self):
        global VersionList
        Widget = QtWidgets.QWidget(self)
        self.setCentralWidget(Widget)
        Hlayout = QtWidgets.QHBoxLayout()
        radioBukkit = QRadioButton('Bukkit')
        radioSpigot = QRadioButton('Spigot')
        radioPaper = QRadioButton('Paper')
        radioInstall = QPushButton('Install')
        Hlayout.addWidget(radioBukkit)
        Hlayout.addWidget(radioSpigot)
        Hlayout.addWidget(radioPaper)
        Hlayout.addWidget(radioInstall)

        Vlayout = QtWidgets.QVBoxLayout(self)
        Vlayout.addLayout(Hlayout)
        self.TBrowser = QtWidgets.QTextBrowser()
        VersionList = QtWidgets.QListWidget()
        self.TBrowser.append("To select a folder go to File->Open")
        Vlayout.addWidget(VersionList)
        Vlayout.addWidget(self.TBrowser)
        Widget.setLayout(Vlayout)
        radioBukkit.clicked.connect(lambda: self.radioAction("Bukkit"))
        radioSpigot.clicked.connect(lambda: self.radioAction("Spigot"))
        radioPaper.clicked.connect(lambda: self.radioAction("Paper"))
        radioInstall.clicked.connect(lambda: self.downloadJar())

    def radioAction(self, buttonPressed):
        global VersionDict
        global buttonSelect
        buttonSelect = buttonPressed
        itemsAdded = []
        Versions = []
        VersionList.clear()
        if buttonPressed == "Bukkit" or buttonPressed == "Spigot":
            for n, i in enumerate(bukkitscrape.requestVersionsBuckkit(buttonPressed)):
                itemsAdded.append(n)
                Versions.append(i)
                VersionDict = dict(zip(Versions,itemsAdded))
                print(VersionDict)
                VersionList.addItem(i)
        else:
            for i in bukkitscrape.requestVersionsPaper():
                VersionList.addItem(i)
        VersionList.itemClicked.connect(self.onClicked)

    def onClicked(self, item):
        global selectedver
        global selectedversiontxt
        if buttonSelect == "Bukkit" or buttonSelect == "Spigot":
            selectedver = VersionDict[item.text()]
            selectedversiontxt = item.text()
            print(selectedver)
        else:
            selectedver = item.text()
            print(selectedver)

    def downloadJar(self):
        print(self.fileSelected)
        if selectedver != None:
            if self.fileSelected != None:
                if buttonSelect == "Bukkit" or buttonSelect == "Spigot":
                    url = bukkitscrape.requestDownloadBuckkit(selectedver)
                    urlstr = "".join(url)
                    urllib.request.urlretrieve(urlstr, self.fileSelected+f"/{buttonSelect}-{selectedversiontxt}.jar")
                    serverGeneration.initalRun(self)
                if buttonSelect == "Paper":
                    urllib.request.urlretrieve(f"https://papermc.io/api/v1/paper/{selectedver}/latest/download", self.fileSelected+f"/Paper-{selectedver}.jar")
                    serverGeneration.initalRun(self)
            else:
                self.TBrowser.append("You must select a folder first!")
        else:
            self.TBrowser.append("You must select a version before installing!")

    def initalRun(self):
        self.p = QtCore.QProcess()
        self.p.setWorkingDirectory(self.fileSelected)
        if buttonSelect == "Paper":
            print('java',['-Xmx1024M', '-Xms1024M', '-jar', f'{self.fileSelected}'+f'/Paper-{selectedver}.jar', '--nogui'])
            self.p.start('java',['-Xmx1024M', '-Xms1024M', '-jar', f'{self.fileSelected}'+f'/Paper-{selectedver}.jar', '--nogui'])
        if buttonSelect == "Bukkit":
            self.p.start('java',['-Xmx1024M', '-Xms1024M', '-jar', f'{self.fileSelected}'+f'/Bukkit-{selectedversiontxt}.jar', '--nogui'])
        if buttonSelect == "Spigot":
            self.p.start('java',['-Xmx1024M', '-Xms1024M', '-jar', f'{self.fileSelected}'+f'/Spigot-{selectedversiontxt}.jar', '--nogui'])
        self.p.readyRead.connect(self.logData)
        
    def logData(self):
        self.TBrowser.append(str(self.p.readAll().data(), encoding="utf-8"))
        self.p.finished.connect(self.finished)

    def finished(self):
        directoryChange.eulaTrue(self)
        subprocess.Popen(["python", "serverHome.py"])
        sys.exit(0)

    def initalFolder(self):
        with open('selectedFile.json') as r:
            temp = json.load(r)
            self.fileSelected = temp['File']
        self.TBrowser.append("Selected Folder: " + self.fileSelected)

    def fileSystem(self):
        self.fileSelected = QFileDialog.getExistingDirectory(self, ("Open Directory"), "/home", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        directoryStore.jsonFileSelected(self)
        self.TBrowser.append("Selected Folder: " + self.fileSelected)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = serverGeneration()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window.show()
    sys.exit(app.exec())
