from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog
import cv2
import numpy as np
import sys
import math
import qimage2ndarray
import threading
from output import Ui_MainWindow


class Window(QtWidgets.QMainWindow):
    changedValue = pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_image)

        # Making the connection
        self.changedValue.connect(self.changeProgressBarValue)

        self.error_dialog = None
        self.divisibleError = None

        self.img = None
        self.fimg_const = None
        self.fimg_original = None
        self.fimg_copy = None

        self.afra7_flag = False
        self.pause_flag = False
        self.lock = threading.Lock()

        self.buttonClick = False

        self.outer_loop_saved = None
        self.inner_loop_saved = None
        self.saveStep = None

        self.step = 0
        self.ui.progressBar.setRange(0, 520)

        self.borderLoops = 1 #for loop functions related to zerooing image
        self.nonDivisible = 0 # related to divisibility

        self.ui.pushButton_2.setText("Pause")

        self.ui.pushButton_2.clicked.connect(self.pauseAndResume)

        self.InitWindow(self)

    def pauseAndResume(self):
        if self.buttonClick == False:
            self.ui.pushButton_2.setText("Resume")
            self.buttonClick = True
            self.pause()
        else:
            self.ui.pushButton_2.setText("Pause")
            self.buttonClick = False
            self.resume()

    @pyqtSlot()
    def changeProgressBarValue(self):
        if self.step >= 520:
            self.step = 0
        self.step = self.step + 1
        self.ui.progressBar.setValue(self.step)

    def closeEvent(self, *args, **kwargs):
        self.afra7_flag = False
        # time.sleep(1)
        # super(Window, self).closeEvent()

    def InitWindow(self, Window):

        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.show()

    def get_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.gif)")
        self.img = cv2.imread(fname[0], 0)
        if self.img is None:
            self.afra7_flag = False
            return self.show_error("الصورة دي مش نافعة يا زميلي")

        if self.img.shape[0] != 520 or self.img.shape[0] != self.img.shape[1]:
            self.afra7_flag = False
            return self.show_error("الابعاد دي متلزمناش يا ساحبي")

        self.afra7_flag = False

        self.ui.progressBar.setValue(0)
        self.step = 0
        # time.sleep(2)

        self.fimg_original = np.fft.fft2(self.img)
        self.fimg_copy = self.fimg_original.copy()
        self.fimg_const = self.fimg_original.copy()

        with self.lock:
            self.show_images()
            threading.Thread(target=self.sho8l_afra7).start()

    def pause(self):
        self.pause_flag = True

    def resume(self):
        if self.pause_flag:
            self.pause_flag = False
            threading.Thread(target=self.sho8l_afra7).start()
    
    def nonDivisibity(self, size):
        
        loops = (int)(self.ui.lineEdit.text())
        dividible = (size*2) % loops
        self.show_error("This number is not divisible by 520 \n \n Hint: \n You could use " + str(dividible) +  " instead")
        self.pauseAndResume()

    def largeInput(self):
        loops = (int)(self.ui.lineEdit.text())
        self.show_error("Out Of Bound Input \n \n Hint: \n PLEASE choose a number smaller than 260")
        self.pauseAndResume()

    def sho8l_afra7(self):
        self.afra7_flag = True
        size = self.fimg_original.shape[0]
        size = size / 2
        size = math.floor(size)

        while True:
            self.step =0
            self.borderLoops = (int)(self.ui.lineEdit.text())
            
            if self.borderLoops > size :
                self.largeInput()
                return

            if size % self.borderLoops != 0:
                self.nonDivisibity(size)
                return
            

            i = 0
            while i < size:

                if self.pause_flag:
                    self.outer_loop_saved = i
                    self.saveStep = self.step
                    return

                if self.inner_loop_saved is not None:
                    break

                if self.outer_loop_saved is not None:
                    i = self.outer_loop_saved
                    self.outer_loop_saved = None
                    self.step = self.saveStep
                    self.saveStep = None

                if not self.afra7_flag:
                    return

                endlimit = i + self.borderLoops
                self.fimg_original[i:endlimit, :] = 0
                self.fimg_original[:, i:endlimit] = 0
                m2loba = self.fimg_original[::-1]
                m2loba[i:endlimit, :] = 0
                self.fimg_original = m2loba[::-1]
                m2loba = np.fliplr(self.fimg_original)
                m2loba[:, i:endlimit] = 0
                self.fimg_original = np.fliplr(m2loba) 
                i = i + self.borderLoops

                self.img = np.fft.ifft2(self.fimg_original).real
                self.fimg_copy = self.fimg_original.copy()
                with self.lock:
                    self.show_images()
                for loop in range(self.borderLoops):
                    if (i - self.borderLoops + loop) < size:
                        self.changedValue.emit()
                if i > size:
                    for loop in range(i - self.borderLoops, size):
                        self.changedValue.emit()

            self.fimg_original = self.fimg_const.copy()
            with self.lock:
                self.show_images()

            j = size - 1
            i = size - self.borderLoops
            while i >= 0:
                if not self.afra7_flag:
                    return
                if self.pause_flag:
                    self.inner_loop_saved = [i, j]
                    self.saveStep = self.step
                    return

                if self.outer_loop_saved is not None:
                    break

                if self.inner_loop_saved is not None:
                    i = self.inner_loop_saved[0]
                    j = self.inner_loop_saved[1]
                    self.inner_loop_saved = None
                    self.step = self.saveStep 
                    self.saveStep = None

                j += self.borderLoops

                self.fimg_original[i:j + 1, i:j + 1] = 0
                self.img = np.fft.ifft2(self.fimg_original).real
                self.fimg_copy = self.fimg_original.copy()
                with self.lock:
                    self.show_images()

                for loop in range(self.borderLoops):
                    self.changedValue.emit()
                i -= self.borderLoops
                if i < 0:
                    for loop in (0, i + self.borderLoops):
                        self.changedValue.emit()
                # time.sleep(0.1)

            self.fimg_original = self.fimg_const.copy()
            with self.lock:
                self.show_images()

    def show_images(self):

        # height, width = img.shape
        # bytesPerLine = 1 * width
        q_img = qimage2ndarray.array2qimage(self.img)
        self.ui.label.setPixmap(QPixmap(q_img))
        # height, width = fimg.shape
        # bytesPerLine = 1 * width
        q_img = qimage2ndarray.array2qimage(self.fimg_copy)
        self.ui.label_2.setPixmap(QPixmap(q_img))
        self.ui.label.show()
        self.ui.label_2.show()

    def show_error(self, error_message):
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setText(error_message)
        self.error_dialog.setWindowTitle("OH NO")
        self.error_dialog.show()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
