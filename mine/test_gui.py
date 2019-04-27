from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Quitter = QtWidgets.QPushButton(self.centralwidget)
        self.Quitter.setGeometry(QtCore.QRect(670, 520, 113, 32))
        self.Quitter.setObjectName("Quitter")
        self.Label = Label(self.centralwidget)
        self.Label.setGeometry(QtCore.QRect(400, 30, 361, 231))
        self.Label.setText("")
        self.Label.setObjectName("Label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Quitter.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Quitter.setText(_translate("MainWindow", "Quitter"))

class Label(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(Label, self).__init__(parent=parent)

    def paintEvent(x):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.red)
        painter.setPen(pen)
        painter.drawEllipse(20, 20, 8, 8)
        painter.end()
        