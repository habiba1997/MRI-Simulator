# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 08:07:53 2019

@author: MM
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
##phantom1
img1 = np.zeros((15,15), np.uint8)
reactangle1=cv2.rectangle(img1,(2,3),(10,12),(60,60,60),-3)
reactangle2=cv2.rectangle(reactangle1,(5,11),(7,14),(208,208,208),-3)
#reactangle3=cv2.rectangle(reactangle2,(50,300),(200,180),(105,105,105),-3)
#phantom1=cv2.rectangle(reactangle3,(170,220),(290,120),(255,255,255),-3)
reactangle2.dump("squares15.dat")
v=np.load("squares15.dat")
plt.imshow(v, plt.cm.gray)
plt.show()

img1 = np.zeros((128,128), np.uint8)
reactangle1=cv2.rectangle(img1,(25,25),(75,62),(42,42,42),-3)
reactangle2=cv2.rectangle(reactangle1,(62,87),(100,50),(32,32,32),-3)
reactangle3=cv2.rectangle(reactangle2,(12,75),(50,45),(26,26,26),-3)
phantom1=cv2.rectangle(reactangle3,(42,55),(72,30),(128,128,128),-3)
phantom1.dump("squares(128).dat")
v=np.load("squares(128).dat")
plt.imshow(v, plt.cm.gray)
plt.show()

img1 = np.zeros((256,256), np.uint8)
reactangle1=cv2.rectangle(img1,(50,50),(150,120),(169,169,169),-3)
reactangle2=cv2.rectangle(reactangle1,(124,180),(200,100),(128,128,128),-3)
reactangle3=cv2.rectangle(reactangle2,(25,150),(100,90),(105,105,105),-3)
phantom1=cv2.rectangle(reactangle3,(80,100),(290,120),(255,255,255),-3)
phantom1.dump("squares(256).dat")
v=np.load("squares(256).dat")
plt.imshow(v, plt.cm.gray)
plt.show()

#phantom2
img2 = np.zeros((128,128), np.uint8)
elipse1=cv2.ellipse(img2,(64,64),(40,55),0,0,360,(255,255,255),-1)
elipse2=cv2.ellipse(elipse1,(64,64),(35,50),0,0,360,(128,128,128),-1)
elipse3=cv2.ellipse(elipse2,(50,65),(7,20),-30,0,360,(0,0,0),-1)
elipse4=cv2.ellipse(elipse3,(80,65),(7,20),30,0,360,(0,0,0),-1)

elipse4.dump("shepplogan(128).dat")
v=np.load("shepplogan(128).dat")
plt.imshow(v, plt.cm.gray)
plt.show()


#phantom2
img2 = np.zeros((512,512), np.uint8)
elipse1=cv2.ellipse(img2,(256,256),(160,220),0,0,360,(255,255,255),-1)
elipse2=cv2.ellipse(elipse1,(256,256),(140,200),0,0,360,(128,128,128),-1)
elipse3=cv2.ellipse(elipse2,(200,260),(28,80),-30,0,360,(0,0,0),-1)
elipse4=cv2.ellipse(elipse3,(320,260),(28,80),30,0,360,(0,0,0),-1)

elipse4.dump("shepplogan(512).dat")
v=np.load("shepplogan(512).dat")
plt.imshow(v, plt.cm.gray)
plt.show()



#phantom2
img2 = np.zeros((256,256), np.uint8)
elipse1=cv2.ellipse(img2,(128,128),(80,110),0,0,360,(255,255,255),-1)
elipse2=cv2.ellipse(elipse1,(128,128),(70,100),0,0,360,(128,128,128),-1)
elipse3=cv2.ellipse(elipse2,(100,130),(14,40),-30,0,360,(0,0,0),-1)
elipse4=cv2.ellipse(elipse3,(160,130),(14,40),30,0,360,(0,0,0),-1)

elipse4.dump("shepplogan(256).dat")
v=np.load("shepplogan(256).dat")
plt.imshow(v, plt.cm.gray)
plt.show()
##phantom3
img = np.zeros((512,512), np.uint8)
line1=cv2.line(img,(400,0),(400,512),(255, 255, 255),15)
line2=cv2.line(img,(0,400),(512,400),(200, 200, 200),30)
circle= cv2.circle(img,(256,256), 120, (169,169,169),-1)
ellipse=cv2.ellipse(img,(200,100),(120,60),0,0,360,(255, 255, 255),-1)

img.dump("circles(512).dat")
v=np.load("circles(512).dat")
plt.imshow(v, plt.cm.gray)
plt.show()
img = np.zeros((256,256), np.uint8)
line1=cv2.line(img,(200,0),(200,256),(255, 255, 255),15)
line2=cv2.line(img,(0,200),(256,200),(200, 200, 200),30)
circle= cv2.circle(img,(128,128), 60, (169,169,169),-1)
ellipse=cv2.ellipse(img,(100,50),(60,30),0,0,360,(255, 255, 255),-1)

img.dump("circles(256).dat")
v=np.load("circles(256).dat")
plt.imshow(v, plt.cm.gray)
plt.show()

img = np.zeros((128,128), np.uint8)
line1=cv2.line(img,(100,0),(100,128),(255, 255, 255),15)
line2=cv2.line(img,(0,100),(128,100),(200, 200, 200),30)
circle= cv2.circle(img,(64,64), 30, (169,169,169),-1)
ellipse=cv2.ellipse(img,(50,25),(30, 15),0,0,360,(255, 255, 255),-1)

img.dump("circles(256).dat")
v=np.load("circles(256).dat")
plt.imshow(v, plt.cm.gray)
plt.show()

##phantom 4(shep logan 40)
img4 = np.zeros((40,40), np.uint8)
elipse1=cv2.ellipse(img4,(20,20),(13,17),0,0,360,(255,255,255),-1)
elipse2=cv2.ellipse(elipse1,(20,20),(11,16),0,0,360,(128,128,128),-1)
elipse3=cv2.ellipse(elipse2,(16,20),(2,0),-30,0,360,(0,0,0),-1)
elipse4=cv2.ellipse(elipse3,(25,20),(2,0),30,0,360,(0,0,0),-1)

elipse4.dump("new_phantom4(40).dat")
v=np.load("phantom4(40).dat")
plt.imshow(v, plt.cm.gray)
plt.show()


#phantom 5(shep logan 60)
img5 = np.zeros((60,60), np.uint8)
elipse1=cv2.ellipse(img5,(32,32),(20,26),0,0,360,(255,255,255),-1)
elipse2=cv2.ellipse(elipse1,(32,32),(18,25),0,0,360,(128,128,128),-1)
elipse3=cv2.ellipse(elipse2,(25,32),(4,10),-30,0,360,(0,0,0),-1)
elipse4=cv2.ellipse(elipse3,(40,32),(4,10),30,0,360,(0,0,0),-1)

elipse4.dump("new_phantom5(60).dat")
v=np.load("phantom5(60).dat")
plt.imshow(v, plt.cm.gray)
plt.show()

#phantom 6(40)
img6 = np.zeros((40,40), np.uint8)
line1=cv2.line(img6,(31,0),(31,13),(255, 255, 255),15)
line2=cv2.line(img6,(0,31),(13,31),(200, 200, 200),30)
circle= cv2.circle(img6,(4,4), 2, (169,169,169),-1)
ellipse=cv2.ellipse(img6,(15,8),(2,1),0,0,360,(255, 255, 255),-1)

img6.dump("new_phantom6(40).dat")
v=np.load("phantom6(40).dat")
plt.imshow(v, plt.cm.gray)
plt.show()



#phantom 7(60)
img7 = np.zeros((60,60), np.uint8)
line1=cv2.line(img7,(44,0),(44,9),(255, 255, 255),15)
line2=cv2.line(img7,(0,44),(9,44),(200, 200, 200),30)
circle= cv2.circle(img7,(20,20), 9, (169,169,169),-1)
ellipse=cv2.ellipse(img7,(3,2),(9,5),0,0,360,(255, 255, 255),-1)

img7.dump("phantom7(40).dat")
v=np.load("phantom7(40).dat")
plt.imshow(v, plt.cm.gray)
plt.show()