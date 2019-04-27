from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from test_gui import *


class MonAppli(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Label.setPixmap(QtGui.QPixmap("43232233_312675282649885_8358144625898160128_n.jpg"))
        self.ui.Label.setScaledContents(True)
        self.ui.Label.paintEvent





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    window.show()
    app.exec_()