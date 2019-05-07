import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class ExcelCheck(QtCore.QThread):
    updated = QtCore.pyqtSignal(int)
    running = False

    def __init__(self, parent=None):
        super(ExcelCheck, self).__init__(parent)
        self.progPercent = 0
        self.running = True

    def run(self):
        while self.running:
            self.progPercent += 1
            self.progPercent %= 100
            self.updated.emit(int(self.progPercent))
            time.sleep(0.1)

    def stop(self):
        self.running = False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.btn_active = False

    def startBtnClicked(self):
        self.btnStart.setText('start!')
        self.btn_active = True
        self.tmr = ExcelCheck(self)
        self.tmr.updated.connect(self.updateValue)
        self.tmr.start()

    def updateValue(self, data):
        self.progressBar.setValue(data)

    def exitBtnClicked(self):
        # self.ExcelCheck()
        self.btn_active = False
        self.tmr.stop()
        self.sys.exit()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(446, 207)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(40, 70, 381, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setGeometry(QtCore.QRect(110, 110, 75, 23))
        self.btnStart.setObjectName("btnStart")
        self.btnStart.clicked.connect(self.startBtnClicked)

        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(260, 110, 75, 23))
        self.btnExit.setObjectName("btnExit")
        self.btnExit.clicked.connect(self.exitBtnClicked)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 446, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SCM21"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        self.btnExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())