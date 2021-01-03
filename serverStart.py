from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import sys
import qdarkstyle
from directoryInfo import directoryStore
import json
import os
import subprocess
class serverStarting(QMainWindow):
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
        self.qBoxButtons()

    def qBoxButtons(self):
        global TBrowser
        global Widget
        Widget = QtWidgets.QWidget(self)
        self.setCentralWidget(Widget)
        Gridlayout = QtWidgets.QGridLayout()

        xmsText = QLabel("XMS = ") #XMS Start
        xmslineRam = QLineEdit('1')
        xmsunitRam = QComboBox()
        xmsText.setMaximumWidth(35)
        xmslineRam.setMaximumWidth(120)
        xmsunitRam.setMaximumWidth(70)
        xmsunitRam.addItems(["G","M","K"])
        self.xmsLineRamText = xmslineRam.text()
        self.xmsRamUnitText = xmsunitRam.currentText()#XMS End

        xmxText = QLabel("XMX = ") #XMX Start
        xmxlineRam = QLineEdit('2')
        xmxunitRam = QComboBox()
        xmxText.setMaximumWidth(35)
        xmxlineRam.setMaximumWidth(120)
        xmxunitRam.setMaximumWidth(70)
        xmxunitRam.addItems(["G","M","K"]) 
        self.xmxLineRamText = xmxlineRam.text()
        self.xmxRamUnitText = xmxunitRam.currentText()#XMX End

        startButton = QPushButton("Start Server") #Start Button
        startButton.clicked.connect(self.serverRun)

        Gridlayout.addWidget(xmsText, 0, 0) #<- XMS-TEXT
        Gridlayout.addWidget(xmslineRam, 0, 1) #<- XMS-LINE
        Gridlayout.addWidget(xmsunitRam, 0, 2) #<- XMS-UNIT

        Gridlayout.addWidget(xmxText, 1, 0) #<- XMX-TEXT
        Gridlayout.addWidget(xmxlineRam, 1, 1) #<-XMX-LINE
        Gridlayout.addWidget(xmxunitRam, 1, 2) #XMX-UNIT

        Gridlayout.addWidget(startButton, 2, 0)
        Widget.setLayout(Gridlayout)

    def serverRun(self):
        with open('selectedFile.json') as r:
            data = json.load(r)
            self.fileSelected = data["File"]
        directoryStore.jsonServerSettings(self)
        subprocess.Popen(["python", "serverStarted.py"])
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = serverStarting()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window.show()
    sys.exit(app.exec())