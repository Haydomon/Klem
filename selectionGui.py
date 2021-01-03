from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import sys
import qdarkstyle
from serverHome import serverHomepage
from directoryInfo import directoryChecks, directoryStore
from generateServer import serverGeneration
import os
import subprocess
import time
import json
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Klem"
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.fileSelected = None
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
        Hlayout = QtWidgets.QHBoxLayout()
        pushSelect = QPushButton('Select Server')
        pushCreate = QPushButton('Create Server')
        Hlayout.addWidget(pushSelect)
        Hlayout.addWidget(pushCreate)

        Vlayout = QtWidgets.QVBoxLayout(self)
        Vlayout.addLayout(Hlayout)
        TBrowser = QtWidgets.QTextBrowser()
        Vlayout.addWidget(TBrowser)
        Widget.setLayout(Vlayout)
        pushSelect.clicked.connect(lambda: self.checkDirectory())
        pushCreate.clicked.connect(lambda: self.genServerOpen())

    def checkDirectory(self):
        if self.fileSelected == None:
            self.fileSystem()
            if directoryChecks.directoryScan(self) == True:
                subprocess.Popen(["python", "serverHome.py"])
                sys.exit(0)
            else:
                self.fileSelected = None
                TBrowser.append("Your selected folder does not contain a Klem generated jar file.")
                TBrowser.append("If you have a server jar please remove it and run create server.")
                TBrowser.append("We recommend you backup your server just in case!")
            
    def genServerOpen(self):
        print("test")
        subprocess.Popen(["python", "generateServer.py"])
        sys.exit(0)

    def fileSystem(self):
        self.fileSelected = QFileDialog.getExistingDirectory(self, ("Open Directory"), "/home", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        directoryStore.jsonFileSelected(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window.show()
    sys.exit(app.exec())