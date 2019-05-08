
from PyQt5 import QtCore, QtGui, QtWidgets
import copy
from PyQt5.QtWidgets import QInputDialog,QFileDialog ,QApplication, QProgressBar , QComboBox , QMessageBox, QAction, QLineEdit
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
from imageio import imsave, imread
from shapeloggin import phantom 
from matplotlib import pyplot as plt


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
        self.ui.browse.clicked.connect (self.browse)
        self.ui.label.mousePressEvent =self.getpos
        self.ui.PhantomShape.currentTextChanged.connect(self.shape)
        self.ui.Preb.currentTextChanged.connect(self.preb)
        self.ui.aquise.currentTextChanged.connect(self.acquisition)

        self.ui.PhantomSize.currentTextChanged.connect(self.phantom_size)
        self.ui.createPhantom.clicked.connect (self.create)
        self.ui.ernstAngle.clicked.connect (self.ernstAngleFun)
        self.ui.start.clicked.connect (self.Start)
        self.ui.horizontalSlider.valueChanged.connect(self.slider)
        self.plotWindow = self.ui.T1
        self.plotWindow2 = self.ui.T2
        self.Acquisition = 0
        self.Prepration = 0
    
    

    def browse(self):
        fileName,_Filter = QtWidgets.QFileDialog.getOpenFileName(None, "Select phantom","","self.data Files(*.dat)")
        if fileName:
            self.data=np.load(fileName)
            self.size=len(self.data)
            self.scale=np.asarray(self.data,dtype=np.uint8)
            image=Image.fromarray(self.scale)
            #print (self.scale)
            self.img= ImageQt(image)
            self.img.save("2.png")
            self.ui.label.setPixmap(QPixmap.fromImage(self.img).scaled(512,512))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
            self.PD=np.asarray(np.load(fileName),dtype=np.uint8)
            self.t1=np.asarray(np.load(fileName),dtype=np.uint8)
            self.t2=np.asarray(np.load(fileName),dtype=np.uint8)
            for i in range (self.size):
               for j in range (self.size):
                   
                   if self.scale[i][j]>=0 and self.scale[i][j]<=50 :
                        self.t1[i][j]=1
                        self.t2[i][j]=50
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


            self.t1 = self.mappingToIntensity(self.t1)
            self.t2 = self.mappingToIntensity(self.t2)

            self.T1_img= gray2qimage(self.t1)
            self.T2_img= gray2qimage(self.t2)
            self.PD_img= gray2qimage(self.scale)

            self.ui.plainTextEdit.clear()
            self.ui.plainTextEdit.appendPlainText(str(np.unique(self.t1)))
            self.ui.plainTextEdit.appendPlainText(str(np.unique(self.t2)))

            self.ui.labelT1.clear()
            self.ui.labelT1.setPixmap(QPixmap.fromImage(self.T1_img).scaled(512,512))
            self.ui.LabelT2.clear()
            self.ui.LabelT2.setPixmap(QPixmap.fromImage(self.T2_img).scaled(512,512))

    
    def mappingToIntensity(self,array):
        maxx = np.max(array)
        minn = np.min(array) 
        array = (((255-2)/(maxx-minn))*(array-minn+2))
        return array

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
        if self.n==0 or self.phantom_type==0 :
             QMessageBox.about(self, "Error", "you should choose the size and shape of the phantom first.")
        else :
            print ("create done ")
        if self.phantom_type==1 and self.n==32:
            elipse4=(phantom(n=32))*1000
            elipse4.dump("shepplogan(32).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(32)'  created and saved ")
        elif self.phantom_type==1 and self.n==9:
            elipse4=(phantom(n=9))*1000
            elipse4.dump("shepplogan(9).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(9)'  created and saved ")
        elif self.phantom_type==1 and self.n==20:
            elipse4=(phantom(n=20))*1000
            elipse4.dump("shepplogan(20).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(20)'  created and saved ")
        elif self.phantom_type==1 and self.n==64:
            elipse4=(phantom(n=64))*1000
            elipse4.dump("shepplogan(64).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(64)'  created and saved ")
        elif self.phantom_type==1 and self.n==512:
            elipse4= phantom(n=512) *1000 
            elipse4.dump("shepplogan(512).dat")
            QMessageBox.about(self, "Done", "phantom 'shepplogan(512)'  created and saved ")    
        elif self.phantom_type==2 and self.n==128:
            self.img1 = np.zeros((128,128), np.uint8)
            reactangle1=cv2.rectangle(self.img1,(25,25),(75,62),(42,42,42),-3)
            reactangle2=cv2.rectangle(reactangle1,(62,87),(100,50),(32,32,32),-3)
            reactangle3=cv2.rectangle(reactangle2,(12,75),(50,45),(26,26,26),-3)
            phantom1=cv2.rectangle(reactangle3,(42,55),(72,30),(128,128,128),-3)
            print(type(phantom1))
            phantom1.dump("squares(128).dat")
            QMessageBox.about(self, "Done", "phantom 'squares(128)'  created and saved ")
        elif self.phantom_type==2 and self.n==256:
            self.img1 = np.zeros((256,256), np.uint8)
            reactangle1=cv2.rectangle(self.img1,(50,50),(150,120),(169,169,169),-3)
            reactangle2=cv2.rectangle(reactangle1,(124,180),(200,100),(128,128,128),-3)
            reactangle3=cv2.rectangle(reactangle2,(25,150),(100,90),(105,105,105),-3)
            phantom1=cv2.rectangle(reactangle3,(80,100),(290,120),(255,255,255),-3)
            phantom1.dump("squares(256).dat")
            print(type(phantom1))
            QMessageBox.about(self, "Done", "phantom 'squares(256)'  created and saved ")
        elif self.phantom_type==2 and self.n==512:
            self.img1 = np.zeros((512,512), np.uint8)
            reactangle1=cv2.rectangle(self.img1,(100,100),(300,150),(169,169,169),-3)
            reactangle2=cv2.rectangle(reactangle1,(250,350),(400,200),(128,128,128),-3)
            reactangle3=cv2.rectangle(reactangle2,(50,300),(200,180),(105,105,105),-3)
            phantom1=cv2.rectangle(reactangle3,(170,220),(290,120),(255,255,255),-3)
            phantom1.dump("squares(512).dat")
            print(type(phantom1))
            QMessageBox.about(self, "Done", "phantom 'squares(512)'  created and saved ")
        elif self.phantom_type==3 and self.n==128:
            self.img = np.zeros((128,128), np.uint8)
            line1=cv2.line(self.img,(100,0),(100,128),(255, 255, 255),15)
            line2=cv2.line(self.img,(0,100),(128,100),(200, 200, 200),30)
            circle= cv2.circle(self.img,(64,64), 30, (169,169,169),-1)
            ellipse=cv2.ellipse(self.img,(50,25),(30, 15),0,0,360,(255, 255, 255),-1)
            print(type(self.img))
            self.img.dump("circles(128).dat")
            QMessageBox.about(self, "Done", "phantom 'circles(128)'  created and saved ")
        elif self.phantom_type==3 and self.n==256:
            self.img = np.zeros((256,256), np.uint8)
            line1=cv2.line(self.img,(200,0),(200,256),(255, 255, 255),15)
            line2=cv2.line(self.img,(0,200),(256,200),(200, 200, 200),30)
            circle= cv2.circle(self.img,(128,128), 60, (169,169,169),-1)
            ellipse=cv2.ellipse(self.img,(100,50),(60,30),0,0,360,(255, 255, 255),-1)
            print(type(self.img))
            self.img.dump("circles(256).dat")
            QMessageBox.about(self, "Done", "phantom 'circles(256)'  created and saved ")
        elif self.phantom_type==3 and self.n==512:
            self.img = np.zeros((512,512), np.uint8)
            line1=cv2.line(self.img,(400,0),(400,512),(255, 255, 255),15)
            line2=cv2.line(self.img,(0,400),(512,400),(200, 200, 200),30)
            circle= cv2.circle(self.img,(256,256), 120, (169,169,169),-1)
            ellipse=cv2.ellipse(self.img,(200,100),(120,60),0,0,360,(255, 255, 255),-1)
            print(type(self.img))
            self.img.dump("circles(512).dat")
            QMessageBox.about(self, "Done", "phantom 'circles(512)'  created and saved ")


    def slider(self):
        self.img2=PIL.Image.open("2.png")
        b=self.ui.horizontalSlider.value()
        print(b)
        enhancer = ImageEnhance.Brightness(self.img2).enhance(b/10)
        enhancer.save("out.png")
        self.ui.label.setPixmap(QPixmap("out.png").scaled(512,512)) 
    
    def getpos (self , event):
         self.x=math.floor((event.pos().x()*self.size)/self.ui.label.frameGeometry().width())
         self.y=math.floor((event.pos().y()*self.size) /self.ui.label.frameGeometry().width())
         self.count=self.count+1
         self.count1=self.count1+1
         self.plot()
         if self.count1==1 :
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(0,255,0), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img).scaled(512,512))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==2:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(0,0,255), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img).scaled(512,512))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==3:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(255,0,0), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img).scaled(512,512))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==4:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(100,255,0), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img).scaled(512,512))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
         elif self.count1==5:
            self.ui.label.clear
            frame=cv2.rectangle(self.scale , (self.x,self.y),(self.x+3,self.y+3),(0,100,100), 1)
            image=Image.fromarray(frame)
            self.img= ImageQt(image)
            self.ui.label.setPixmap(QPixmap.fromImage(self.img).scaled(512,512))
            self.ui.label.setAlignment(QtCore.Qt.AlignCenter)
            self.count1=0
         else :
            print ('end')
    
    def plot(self):
        arr1 = []
        arr2 = []
        self.FA() 
        self.Time_span()
        fa=(np.pi)*self.f/180 
        for t in range (self.T):
            self.Mz=(1-np.exp(-t/self.t1[self.x,self.y]))
            Rx=np.array([[1, 0, 0] ,[0, (np.cos(fa)), (np.sin(fa))], [0 ,(-np.sin(fa)) ,(np.cos(fa))]])
            M=np.matmul(Rx,self.signal[self.x][self.y])
            M=np.sum(M)
            Mxy=np.exp(-t/self.t2[self.x,self.y])*M
            arr1.append(self.Mz)
            arr2.append(Mxy)
#            QtGui.QApplication.processEvents()
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
            
    def ernstAngleFun(self):
            self.TR()
            vector= np.dot (130,np.matrix ([0,0,1])) 
            step = 5
            intensity = np.zeros(int(180/step))
            j =0
            for theta in range ( 0, 180 , step ):
                for i in range(10):
                    vector = self.rotationAroundYaxisMatrix(theta,vector)
                    vector = self.DecayRecoveryEquation(2600,50,1,vector,self.tr)
                
                x = np.ravel(vector)[0]
                y = np.ravel(vector)[1]
                intensity[j] = math.sqrt((x*x)+(y*y))
                j+=1        
            array = np.arange(0,180,step)
            plt.plot(array,intensity)
            plt.show()
            #QMessageBox.about(self, "Error", "you should choose the sequence first")
             

    def rotationAroundYaxisMatrix(self,theta,vector):
            vector = vector.transpose()
            theta = (math.pi / 180) * theta
            R = np.matrix ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]] )
            R = np.dot(R, vector)
            R = R.transpose()
            return np.matrix(R)

    def rotationAroundZaxisMatrixXY(self,TR,speed,vector,time): #time = self.time
            vector = vector.transpose()
            theta = speed * (time/ TR)
            theta = (math.pi / 180) * theta
            XY = np.matrix([[np.cos(theta),-np.sin(theta),0], [np.sin(theta), np.cos(theta),0],[0, 0, 1]])
            XY = np.dot(XY,vector)
            XY = XY.transpose()
            return np.matrix(XY) 


    def DecayRecoveryEquation(self,T1,T2,PD,vector,time):
            vector = vector.transpose()
            Decay =np.matrix([[np.exp(-time/T2),0,0],[0,np.exp(-time/T2),0],[0,0,np.exp(-time/T1)]])
            Decay = np.dot(Decay,vector)
        
            Rec= np.dot(np.matrix([[0,0,(1-(np.exp(-time/T1)))]]),PD)
            Rec = Rec.transpose()
            Decay = np.matrix(Decay)
            Rec =  np.matrix(Rec)    
        
            RD  = Decay + Rec
            RD = RD.transpose()
            return RD

    def TR(self):    
        self.tr=self.ui.TR.value()

        
    def TE(self):
        self.te=self.ui.TE.value()
       
        
    def FA(self):
        self.f=self.ui.FA.value()
        
    def Time_span(self):
        self.T=self.ui.time_span.value()
        print(self.T)
    
    def acquisition (self,text):
        
        if text =="SSFP":
            self.Acquisition=1
        elif text=="SpinEcho": #squares
            self.Acquisition=2
        elif text=="GRE": #circles
            self.Acquisition=3
        else: 
            self.Acquisition = 0
    
    def preb (self,text):
        if text=="T1IR": #squares
            self.Prepration=1
            self.nullTissue, ok = QInputDialog.getInt(self,"integer input dialog","enter Null Tissue T1")
            print(self.nullTissue)
        elif text=="T2Preb": #circles
            self.Prepration=2
            self.T2prebtime, ok = QInputDialog.getInt(self,"integer input dialog","enter time inteval for preb")
            print(self.T2prebtime)
        elif text=="Tagging":
            self.Prepration=3
        else: 
            self.Prepration =0 

    def prepration(self):
        if (self.Prepration==1):
            t = self.nullTissue * np.log(2)
            for i in range(self.size):
                    for j in range(self.size):
                        self.signal[i][j] = self.rotationAroundYaxisMatrix(180,np.matrix(self.signal[i][j])) 
                        self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),t)
                        self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]
        
        elif (self.Prepration==2):
            for i in range(self.size):
                    for j in range(self.size):
                        self.signal[i][j] = self.rotationAroundYaxisMatrix(90,np.matrix(self.signal[i][j])) 
                        self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),self.T2prebtime)
                        self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]
                        self.signal[i][j] = self.rotationAroundYaxisMatrix(-90,np.matrix(self.signal[i][j])) 
        elif (self.Prepration==0):
            print("nrg3 normal tany")
        elif (self.Prepration==3):
            print("tagging")
        else:
            QMessageBox.about(self, "Error", "you should choose the Preperation sequence first")

        
      

    def startUpCycle(self):
        self.StartUpCycle=self.ui.StartUpCycle_2.value()
        self.signal = [[[0 for k in range(3)] for j in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
                for j in range(self.size):
                    self.signal[i][j][2] =1
       
        for loop in range(self.StartUpCycle):
                    for i in range(self.size):
                        for j in range(self.size):
                            self.signal[i][j] = self.rotationAroundYaxisMatrix(self.f,np.matrix(self.signal[i][j])) 
                            self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),self.tr)
                            self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]
       

    def Start(self):
        
        self.TE() 
        self.TR()
        self.FA() 
        self.Kspace =  np.zeros((self.size,self.size),dtype=np.complex_)
        self.startUpCycle()
        self.prepration()
        if (self.Acquisition==1):
            self.SSFPForLoops()
        elif (self.Acquisition==2):
            self.SpinEchoForLoops()
        elif (self.Acquisition==3):
            self.GREForLoops()
        else:
            QMessageBox.about(self, "Error", "you should choose the acquisition sequence first")
    
    def SpinEchoForLoops(self):    

        for Ki in range(self.Kspace.shape[0]):
            print('Ki: ',Ki)

            for i in range(self.size):
                    for j in range(self.size):
                        self.signal[i][j] =  self.rotationAroundYaxisMatrix(self.f,np.matrix(self.signal[i][j]))
                        self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),(self.te/2))
                        self.signal[i][j] =  self.rotationAroundYaxisMatrix((self.f*2),np.matrix(self.signal[i][j]))
                        self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),(self.te/2))

            # for kspace column
            for Kj in range ( self.Kspace.shape[1]):
                print('Kj: ',Kj)
                GxStep = ((2 * math.pi) /  self.Kspace.shape[0]) * Kj
                GyStep = ((2 * math.pi) / self.Kspace.shape[1]) * Ki            
                
                for i in range(self.size):
                    for j in range(self.size):
                        totalTheta = (GxStep*j)+ (GyStep*i)
                        z = abs(complex(np.ravel(self.signal[i][j])[0],np.ravel(self.signal[i][j])[1]))
                        self.Kspace[Ki,Kj]= self.Kspace[Ki,Kj] + (z * np.exp(1j*totalTheta))
            
            for i in range(self.size):
                for j in range(self.size):
                    self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),(self.tr))
                    self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]


        self.ReconstructionImageAndKspace()

    def SSFPForLoops(self):    
        angle60 = True

        for i in range(self.size):
            for j in range(self.size):
                self.signal[i][j] =  self.rotationAroundYaxisMatrix((self.f/2),np.matrix(self.signal[i][j]))
                self.signal[i][j] =  self.DecayRecoveryEquation(self.t1[i][j],self.t2[i][j],1,np.matrix(self.signal[i][j]),self.tr)
                self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]
        
        for Ki in range(self.Kspace.shape[0]):
            print('Ki: ',Ki)
            #move in each image pixel            
            if angle60 :
                theta = -self.f
            else:
                theta = self.f
                
            for i in range(self.size):
                    for j in range(self.size):
                        self.signal[i][j] =  self.rotationAroundYaxisMatrix(theta,np.matrix(self.signal[i][j]))
                        self.signal[i][j] = self.signal[i][j] * np.exp(-self.te/self.t2[i][j])


            # for kspace column
            for Kj in range ( self.Kspace.shape[1]):
                print('Kj: ',Kj)
                GxStep = ((2 * math.pi) /  self.Kspace.shape[0]) * Kj
                GyStep = ((2 * math.pi) / self.Kspace.shape[1]) * Ki            
                
                for i in range(self.size):
                    for j in range(self.size):
                        totalTheta = (GxStep*j)+ (GyStep*i)
                        z = abs(complex(np.ravel(self.signal[i][j])[0],np.ravel(self.signal[i][j])[1]))
                        self.Kspace[Ki,Kj]= self.Kspace[Ki,Kj] + (z * np.exp(1j*totalTheta))
            
            for i in range(self.size):
                for j in range(self.size):
                    self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),(self.tr))
                    self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]

            angle60 = not angle60

        self.ReconstructionImageAndKspace()
    
    
    def GREForLoops(self): 

        for Ki in range(self.Kspace.shape[0]):
            print('Ki: ',Ki)
            #move in each image pixel            

            for i in range(self.size):
                for j in range(self.size):
                        self.signal[i][j] =  self.rotationAroundYaxisMatrix(self.f,np.matrix(self.signal[i][j]))
                        self.signal[i][j] = self.signal[i][j] * np.exp(-self.te/self.t2[i][j])

            # for kspace column
            for Kj in range (self.Kspace.shape[1]):
                print('Kj: ',Kj)
                GxStep = ((2 * math.pi) / self.Kspace.shape[0]) * Kj
                GyStep = ((2 * math.pi) /self.Kspace.shape[1]) * Ki
                
                
                for i in range(self.size):
                    for j in range(self.size):
                        totalTheta = (GxStep*j)+ (GyStep*i)
                        z = abs(complex(np.ravel(self.signal[i][j])[0],np.ravel(self.signal[i][j])[1]))
                        self.Kspace[Ki,Kj]= self.Kspace[Ki,Kj] + (z * np.exp(1j*totalTheta))

            for i in range(self.size):
                for j in range(self.size):
                    self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i,j],self.t2[i,j],1,np.matrix(self.signal[i][j]),(self.tr))
                    self.signal[i][j] = [[0,0,np.ravel(self.signal[i][j])[2]]]
        
        self.ReconstructionImageAndKspace()

    
    def ReconstructionImageAndKspace(self):
        print(self.Kspace)
        KspaceSave =abs(copy.deepcopy(self.Kspace))
        print("Done")
        imsave('kspace.png', KspaceSave)
        self.ui.label_2.setPixmap(QtGui.QPixmap('kspace.png').scaled(512,512))
        Kspacefft = np.fft.fft2(self.Kspace)
        #Kspaceifft = np.fft.ifft2(self.Kspace)
        Kspacefft = abs(Kspacefft)
        Kspacefft = self.mappingToIntensity(np.array(np.round_(Kspacefft)))
        imsave("image.png", Kspacefft)

        pixmap = QtGui.QPixmap("image.png")
        pixmap = pixmap.scaled(512,512)
        self.ui.label_3.setPixmap(pixmap)

            
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()