from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect, QProcess
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import sys
import qdarkstyle
import subprocess
import json
from directoryInfo import directoryGrab
import asyncio
import os
class serverManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Klem"
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initWindow()
        self.grabDataSet()
        self.start()

    def initWindow(self):
        self.setWindowIcon(QtGui.QIcon("tree.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.qBoxButtons()

    def qBoxButtons(self):
        self.Widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.Widget)
        Hlayout = QtWidgets.QHBoxLayout()
        Vlayout = QtWidgets.QVBoxLayout()
        Vlayout.addLayout(Hlayout)

        self.TBrowser = QtWidgets.QTextBrowser()
        self.cmdLine = QtWidgets.QLineEdit(self)
        self.cmdLine.returnPressed.connect(self.sendCMD)
        stopButton = QPushButton("Stop Server") #Stop Button
        Vlayout.addWidget(self.cmdLine)
        Vlayout.addWidget(stopButton)
        stopButton.clicked.connect(self.stop)
        Hlayout.addWidget(self.TBrowser)
        self.Widget.setLayout(Vlayout)

    def grabDataSet(self):
        global jarFile
        with open('selectedFile.json') as r:
            data = json.load(r)
            self.fileSelected = data["File"]
            self.xmxLineRamText = data["xmxLineRam"]
            self.xmxRamUnitText = data["xmxRamUnit"]
            self.xmsLineRamText = data["xmsLineRam"]
            self.xmsRamUnitText = data["xmsRamUnit"]
            jarFile = directoryGrab.DirectorySearchForJar(self)
            print(jarFile)

    def start(self):
        self.p = QtCore.QProcess()
        self.p.setWorkingDirectory(self.fileSelected)
        self.p.start('java',
        ['-Xmx'+f'{self.xmxLineRamText}'+f'{self.xmxRamUnitText}',
        '-Xms'+f'{self.xmsLineRamText}'+f'{self.xmsRamUnitText}',
        '-jar',
        f'{self.fileSelected}'+f'/{jarFile}', 
        '--nogui'])
        self.p.readyRead.connect(self.logData)

    def logData(self):
        self.TBrowser.append(str(self.p.readAll().data(), encoding="utf-8"))

    def sendCMD(self):
        if self.cmdLine.text().lower() == "stop":
                self.stop()
        else:
            self.p.write((self.cmdLine.text()+"\n").encode())
            self.cmdLine.clear()

    def stop(self):
        print("TEST")
        self.p.write('stop\n'.encode())
        subprocess.Popen(["python", "serverHome.py"])
        sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = serverManagement()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window.show()
    sys.exit(app.exec())