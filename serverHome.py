from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5 import QtCore, uic, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import sys
import qdarkstyle
import subprocess
class serverHomepage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Klem"
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 400
        self.initWindow()
        self.fileSelected = None

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
        Vlayout = QtWidgets.QVBoxLayout()
        pushStart = QPushButton('Start Server')
        pushInstall = QPushButton('Install Plugins')
        pushUpdate = QPushButton('Manage Plugins')
        pushMarket = QPushButton('MarketPlace')
        pushDiscord = QPushButton('Discord')
        pushPatreon = QPushButton('Patreon')
        Vlayout.addWidget(pushStart)
        Vlayout.addWidget(pushInstall)
        Vlayout.addWidget(pushUpdate)
        Vlayout.addWidget(pushMarket)
        Vlayout.addWidget(pushDiscord)
        Vlayout.addWidget(pushPatreon)
        Widget.setLayout(Vlayout)
        pushStart.clicked.connect(lambda: self.sectionSelected("start"))

    def sectionSelected(self, buttonPressed):
        if buttonPressed == "start":
            subprocess.Popen(["python", "serverStart.py"])
            sys.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = serverHomepage()
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window.show()
    sys.exit(app.exec())