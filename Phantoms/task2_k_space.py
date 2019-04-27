
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog ,QApplication, QProgressBar , QComboBox , QMessageBox, QAction, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSlot
from Digital_phantom2 import Ui_MainWindow
import sys
import time
import math
import cv2
import pyqtgraph as pg
import numpy as np
from PIL.ImageQt import ImageQt
from PIL import Image, ImageEnhance
import PIL
from qimage2ndarray import gray2qimage
m=0
class ApplicationWindow (QtWidgets.QMainWindow):
    @pyqtSlot()        
    def __init__(self):
        self.count=0
        self.count1=0
        self.n=0
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect (self.browse)
        self.ui.comboBox_2.currentTextChanged.connect(self.Property)
        self.ui.label.mousePressEvent =self.getpos
        self.ui.comboBox.currentTextChanged.connect(self.shape)
        self.ui.comboBox_3.currentTextChanged.connect(self.phantom_size)
        self.ui.pushButton.clicked.connect (self.create)
        self.ui.pushButton_3.clicked.connect (self.Start)
        self.ui.horizontalSlider.valueChanged.connect(self.slider)
        
        
    
    def browse(self):
        fileName,_Filter = QtWidgets.QFileDialog.getOpenFileName(None, "Select phantom","","self.data Files(*.dat)")
        if fileName:
            """
            #global self.PD_img
            #global self.PD 
            global Mo = self.signal
            global self.empty_matrix
            global self.K_space 
            """
            self.data=np.load(fileName)
            self.size=len(self.data)
            self.scale=np.asarray(self.data,dtype=np.uint8)
            image=Image.fromarray(self.scale)
            print (self.scale)
            self.img= ImageQt(image)
            self.img.save("2.png")
            self.ui.label.setPixmap(QPixmap.fromImage(self.img))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
            self.K_space=np.empty([self.size,self.size] , dtype= complex)
            self.empty_matrix=np.asarray(np.load(fileName),dtype=np.uint8)
            self.PD=np.asarray(np.load(fileName),dtype=np.uint8)
            self.t1=np.asarray(np.load(fileName),dtype=np.uint8)
            self.t2=np.asarray(np.load(fileName),dtype=np.uint8)
            self.signal=[[[0 for k in range(3)] for j in range(self.size)] for i in range(self.size)]
            for i in range (self.size):
               for j in range (self.size):
                   self.signal[i][j][2]=1
                   self.empty_matrix[i][j]=255
                   self.K_space[i,j]=0
                   if self.scale[i][j]>=0 and self.scale[i][j]<=50 :
                       self.t1[i][j]=1000
                       self.t2[i][j]=100
                   elif self.scale[i][j]<=100 and self.scale[i][j] >=50:
                       self.t1[i][j]=1200
                       self.t2[i][j]=120
                   elif self.scale[i][j] <=150 and self.scale[i][j] >=100 :
                        self.t1[i,j]=1300
                        self.t2[i,j]=150
                   elif self.scale[i,j] <=200 and self.scale[i,j] >=150:
                        self.t1[i,j]=1500
                        self.t2[i,j]=170
                   elif self.scale[i,j] <=255 and self.scale[i,j] >=200:
                        self.t1[i,j]=2000
                        self.t2[i,j]=200
                   else:
                        break 
            self.T1_img=  gray2qimage(self.t1)
            self.T2_img= gray2qimage(self.t2)
            self.PD_img= gray2qimage(self.scale)
            
    def phantom_size(self, text):
        print(text)
        self.n=int(text) 
        
        
    def shape(self, text):
        print(text)
        #self.phantom_type
        if text=="Shepp-Logan":
            self.phantom_type=1
        elif text=="Phantom 1": #squares
            self.phantom_type=2
        elif text=="phantom 2": #circles
            self.phantom_type=3
        else: 
            self.phantom_type=0
    
    
    def create(self):
        """
        global self.n
        global self.phantom_type
        self.scale
        self.data
        global self.size
        self.T1_img2
        self.T2_img2
        #global self.PD_img2
        global self.t1
        global self.t2 
        #global self.PD 
        global self.signal
        global self.empty_matrix
        """
        if self.n==0 or self.phantom_type==0 :
             QMessageBox.about(self, "Error", "you should choose the size and shape of the phantom first.")
        else :
            print ("create done ")
        if self.phantom_type==1 and self.n==128:
            self.img2 = np.zeros((128,128), np.uint8)
            elipse1=cv2.ellipse(self.img2,(64,64),(40,55),0,0,360,(255,255,255),-1)
            elipse2=cv2.ellipse(elipse1,(64,64),(35,50),0,0,360,(128,128,128),-1)
            elipse3=cv2.ellipse(elipse2,(50,65),(7,20),-30,0,360,(0,0,0),-1)
            elipse4=cv2.ellipse(elipse3,(80,65),(7,20),30,0,360,(0,0,0),-1)
            elipse4.dump("shepplogan(128).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(128)'  created and saved ")
        elif self.phantom_type==1 and self.n==256:
            self.img2 = np.zeros((256,256), np.uint8)
            elipse1=cv2.ellipse(self.img2,(128,128),(80,110),0,0,360,(255,255,255),-1)
            elipse2=cv2.ellipse(elipse1,(128,128),(70,100),0,0,360,(128,128,128),-1)
            elipse3=cv2.ellipse(elipse2,(100,130),(14,40),-30,0,360,(0,0,0),-1)
            elipse4=cv2.ellipse(elipse3,(160,130),(14,40),30,0,360,(0,0,0),-1)

            elipse4.dump("shepplogan(256).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(256)'  created and saved ")
        elif self.phantom_type==1 and self.n==512:
            self.img2 = np.zeros((512,512), np.uint8)
            elipse1=cv2.ellipse(self.img2,(256,256),(160,220),0,0,360,(255,255,255),-1)
            elipse2=cv2.ellipse(elipse1,(256,256),(140,200),0,0,360,(128,128,128),-1)
            elipse3=cv2.ellipse(elipse2,(200,260),(28,80),-30,0,360,(0,0,0),-1)
            elipse4=cv2.ellipse(elipse3,(320,260),(28,80),30,0,360,(0,0,0),-1)

            elipse4.dump("shepplogan(512).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(512)'  created and saved ")    
        elif self.phantom_type==2 and self.n==128:
            self.img1 = np.zeros((128,128), np.uint8)
            reactangle1=cv2.rectangle(self.img1,(25,25),(75,62),(42,42,42),-3)
            reactangle2=cv2.rectangle(reactangle1,(62,87),(100,50),(32,32,32),-3)
            reactangle3=cv2.rectangle(reactangle2,(12,75),(50,45),(26,26,26),-3)
            phantom1=cv2.rectangle(reactangle3,(42,55),(72,30),(128,128,128),-3)
            phantom1.dump("squares(128).dat")
            QMessageBox.about(self, "Done", "phantom 'squares(128)'  created and saved ")
        elif self.phantom_type==2 and self.n==256:
            self.img1 = np.zeros((256,256), np.uint8)
            reactangle1=cv2.rectangle(self.img1,(50,50),(150,120),(169,169,169),-3)
            reactangle2=cv2.rectangle(reactangle1,(124,180),(200,100),(128,128,128),-3)
            reactangle3=cv2.rectangle(reactangle2,(25,150),(100,90),(105,105,105),-3)
            phantom1=cv2.rectangle(reactangle3,(80,100),(290,120),(255,255,255),-3)
            phantom1.dump("squares(256).dat")
            QMessageBox.about(self, "Done", "phantom 'squares(256)'  created and saved ")
        elif self.phantom_type==2 and self.n==512:
            self.img1 = np.zeros((512,512), np.uint8)
            reactangle1=cv2.rectangle(self.img1,(100,100),(300,150),(169,169,169),-3)
            reactangle2=cv2.rectangle(reactangle1,(250,350),(400,200),(128,128,128),-3)
            reactangle3=cv2.rectangle(reactangle2,(50,300),(200,180),(105,105,105),-3)
            phantom1=cv2.rectangle(reactangle3,(170,220),(290,120),(255,255,255),-3)
            phantom1.dump("squares(512).dat")
            QMessageBox.about(self, "Done", "phantom 'squares(512)'  created and saved ")
            
        elif self.phantom_type==3 and self.n==128:
            self.img = np.zeros((128,128), np.uint8)
            line1=cv2.line(self.img,(100,0),(100,128),(255, 255, 255),15)
            line2=cv2.line(self.img,(0,100),(128,100),(200, 200, 200),30)
            circle= cv2.circle(self.img,(64,64), 30, (169,169,169),-1)
            ellipse=cv2.ellipse(self.img,(50,25),(30, 15),0,0,360,(255, 255, 255),-1)

            self.img.dump("circles(128).dat")
            QMessageBox.about(self, "Done", "phantom 'circles(128)'  created and saved ")
        elif self.phantom_type==3 and self.n==256:
            self.img = np.zeros((256,256), np.uint8)
            line1=cv2.line(self.img,(200,0),(200,256),(255, 255, 255),15)
            line2=cv2.line(self.img,(0,200),(256,200),(200, 200, 200),30)
            circle= cv2.circle(self.img,(128,128), 60, (169,169,169),-1)
            ellipse=cv2.ellipse(self.img,(100,50),(60,30),0,0,360,(255, 255, 255),-1)

            self.img.dump("circles(256).dat")
            QMessageBox.about(self, "Done", "phantom 'circles(256)'  created and saved ")
        elif self.phantom_type==3 and n==512:
            self.img = np.zeros((512,512), np.uint8)
            line1=cv2.line(self.img,(400,0),(400,512),(255, 255, 255),15)
            line2=cv2.line(self.img,(0,400),(512,400),(200, 200, 200),30)
            circle= cv2.circle(self.img,(256,256), 120, (169,169,169),-1)
            ellipse=cv2.ellipse(self.img,(200,100),(120,60),0,0,360,(255, 255, 255),-1)

            self.img.dump("circles(512).dat")
            QMessageBox.about(self, "Done", "phantom 'circles(512)'  created and saved ")
     

            
    def Property(self, text):
           print("start")
           """self.T1_img
           self.T2_img
           #global self.PD_img
           self.img
           self.T1_img2
           self.T2_img2
           #global self.PD_img2"""
           type=text
           if type=='T1':
              self.ui.label.clear()
              self.ui.label.setPixmap(QPixmap.fromImage(self.T1_img))
           if type=='T2':
              self.ui.label.clear()
              self.ui.label.setPixmap(QPixmap.fromImage(self.T2_img))
           if type=='self.PD':
              self.ui.label.clear()
              self.ui.label.setPixmap(QPixmap.fromImage(self.PD_img))
    def slider(self):
        self.img2=PIL.Image.open("2.png")
        b=self.ui.horizontalSlider.value()
        print(b)
        enhancer = ImageEnhance.Brightness(self.img2).enhance(b/10)
        enhancer.save("out.png")
        self.ui.label.setPixmap(QPixmap("out.png")) 
    
    def getpos (self , event):
         """global x
         global self.y
         global self.count
         self.size
         global self.count1"""

         self.x=math.floor((event.pos().x()*self.size)/self.ui.label.frameGeometry().width())
         self.y=math.floor((event.pos().y()*self.size) /self.ui.label.frameGeometry().width())
         self.count=self.count+1
         self.count1=self.count1+1
         self.x=self.x
         self.y=self.y
         self.plot()
         if self.count1==1 :
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(0,255,0), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==2:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(0,0,255), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==3:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(255,0,0), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==4:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(100,255,0), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==5:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(0,100,100), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
            self.count1=0
         else :
            print ('end')
    def plot(self):
        """
        global self.x
        global self.y
        global self.t1
        global self.t2 
        #global self.PD
        global self.size
        global self.f
        global self.signal
        global self.Mz
        global T
        """
        arr1 = []
        arr2 = []
        self.FA() 
        self.Time_span()
        fa=(np.pi)*self.f/180
        #global self.count
        #global self.plotWindow 
        #global self.plotWindow2 
        self.plotWindow = self.ui.T1
        self.plotWindow2 = self.ui.T2
        for t in range (self.T):
            self.Mz=(1-np.exp(-t/self.t1[self.x,self.y]))
            Rx=np.array([[1, 0, 0] ,[0, (np.cos(fa)), (np.sin(fa))], [0 ,(-np.sin(fa)) ,(np.cos(fa))]])
            M=np.matmul(Rx,self.signal[self.x][self.y])
            M=np.sum(M)
            Mxy=np.exp(-t/self.t2[self.x,self.y])*M
            arr1.append(self.Mz)
            arr2.append(Mxy)
#            QtGui.QApplication.processEvents()
#            time.sleep(0.2)
        if self.count==1 :
            self.plotWindow.clear()
            self.plotWindow2.clear()
            self.plotWindow.plot(arr1, pen=pg.mkPen('b', width=2))
            self.plotWindow2.plot(arr2, pen=pg.mkPen('b', width=2))
        elif self.count==2:
            self.plotWindow.plot(arr1, pen1=pg.mkPen('r', width=2))
            self.plotWindow2.plot(arr2, pen1=pg.mkPen('r', width=2))
        elif self.count==3:
            self.plotWindow.plot(arr1, pen2=pg.mkPen('g', width=2))
            self.plotWindow2.plot(arr2, pen2=pg.mkPen('g', width=2))
        elif self.count==4:
            self.plotWindow.plot(arr1, pen=pg.mkPen('l', width=2))
            self.plotWindow2.plot(arr2, pen=pg.mkPen('l', width=2))
        elif self.count==5:
            self.plotWindow.plot(arr1, pen=pg.mkPen('w', width=2))
            self.plotWindow2.plot(arr2, pen=pg.mkPen('w', width=2))
            self.count=0
        else :
            print ('end') 
        self.TE() 
        self.TR()  
            
            
            
    def TR(self):
        #global self.tr 
        #global self.plotWindow 
        #global self.plotWindow2        
        self.tr=self.ui.TR.value()
        print(self.tr)
        self.plotWindow.plot([self.tr,self.tr],[0,1], pen=pg.mkPen('r', width=3))   
        self.plotWindow2.plot([self.tr,self.tr],[-1,1], pen=pg.mkPen('r', width=3))
        
    def TE(self):
        #global self.te
        #global self.Mz
        self.te=self.ui.TE.value()
        self.plotWindow.plot([self.te,self.te],[0,1], pen=pg.mkPen('b', width=3)) 
        self.plotWindow2.plot([self.te,self.te],[-1,1], pen=pg.mkPen('b', width=3))
        
    def FA(self):
        self.f=self.ui.FA.value()
        print( self.f)
        
    def Time_span(self):
        self.T=self.ui.time_span.value()
        print(self.T)
        
    def Start(self): 
      """
      global self.tr
      global self.te
      global self.t1
      global self.t2 
      #global self.PD
      global self.size
      global self.f
      global self.signal
      global self.Mz
      global T
      global K
      global self.K_space
      global empty
      """
      K=1j
      self.TE() 
      self.TR()
      self.FA() 
      fa=(np.pi)*self.f/180
      rx=np.array([[1, 0, 0] ,[0, np.cos(fa), (np.sin(fa))], [0 ,(-np.sin(fa)) ,(np.cos(fa))]]) 
      rotate_by_FA=[[[0 for k in range(3)] for j in range(self.size)] for i in range(self.size)]
      result=[[[0 for k in range(3)] for j in range(self.size)] for i in range(self.size)]
      empty1=  gray2qimage(self.empty_matrix)
      self.ui.label_2.setPixmap(QPixmap.fromImage(empty1))
      print("start")
      for self.K_space_Row in range(self.size):
          for i in range (self.size):
             for j in range (self.size):
                mat1=np.matmul(rx,self.signal[i][j]) #rotate by flip angle around X
                rotate_by_FA[i][j]=mat1
          for i in range (self.size):
             for j in range (self.size):
                 Decay_Matrix=np.array([[np.exp(-self.te/self.t2[i,j]), 0, 0], [0, np.exp(-self.te/self.t2[i,j]),0],[0 ,0 ,np.exp(-self.te/self.t1[i,j])]])
                 mat2=np.matmul(Decay_Matrix,rotate_by_FA[i][j])
                 result[i][j]=mat2
          for self.K_space_column in range(self.size):
              Gx_Step=(2*np.pi/self.size)*self.K_space_Row
              Gy_Step=(2*np.pi/self.size)*self.K_space_column
              for i in range (self.size):
                 for j in range (self.size):
                    theta = Gx_Step * i + Gy_Step * j
                    self.K_space[-self.K_space_Row,-self.K_space_column]+=(math.sqrt((result[i][j][0])*(result[i][j][0])+(result[i][j][1])*(result[i][j][1])))*(np.exp(K*theta))
              self.empty_matrix[self.K_space_Row][self.K_space_column]=self.K_space[-self.K_space_Row,-self.K_space_column]
              self.img2=np.asarray(abs(self.empty_matrix),dtype=np.uint8)
              image2=Image.fromarray(self.img2)
              Result2= ImageQt(image2)
              '''
              self.ui.label_2.setPixmap(QPixmap.fromImage(Result2))
              self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
              QApplication.processEvents()
              time.sleep(0.2)
              '''
          for i in range (self.size):
             for j in range (self.data):
               result[i][j][0]=0
               result[i][j][1]=0 
               result[i][j][2]= 1-np.exp(-self.tr/self.t1[i,j]) 
      self.ui.label_2.setPixmap(QPixmap.fromImage(Result2))
      self.ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
      QApplication.processEvents()
      recon= np.fft.ifft2(self.K_space).real
      print (recon)
      ans=recon*1000
      self.img3=np.asarray(ans,dtype=np.uint8)
      print(self.img3)
      image3=Image.fromarray(self.img3)
      Result3= ImageQt(image3)
      self.ui.label_3.setPixmap(QPixmap.fromImage(Result3))
      self.ui.label_3.setAlignment(QtCore.Qt.AlignCenter) 
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()