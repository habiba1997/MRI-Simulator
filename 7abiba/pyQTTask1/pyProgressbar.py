import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QBasicTimer
import time


class App(QWidget):
 
 def __init__(self):
  super().__init__()
  self.progressBar = QProgressBar(self)
  self.progressBar.setGeometry(30,40,200,25)
  
  self.btnStart =QPushButton('start',self)
  self.btnStart.move(40,80)
  self.btnStart.clicked.connect(self.startProgress)

  self.btnEnd =QPushButton('End',self)
  self.btnEnd.move(100,130)
  self.btnEnd.clicked.connect(self.endProgress)

  self.step = 0

 def endProgress(self):
    self.step =0
    self.progressBar.setValue(self.step)

 def startProgress(self):
  for i in range(0, 54):
      self.progressBar.setValue(i)
      
 



if __name__ == '__main__':
 app = QApplication(sys.argv)
 ex = App()
 ex.show()
 sys.exit(app.exec_())