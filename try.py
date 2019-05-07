import numpy as np
from shapeloggin import phantom 
from matplotlib import pyplot as plt
import math
""""
def rotationAroundYaxisMatrix(theta,vector):
            vector = vector.transpose()
            theta = (math.pi / 180) * theta
            R = np.matrix ([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]] )
            R = np.dot(R, vector)
            R = R.transpose()
            return np.matrix(R)


def rotationAroundZaxisMatrixXY(TR,speed,vector,time): #time = self.time
            vector = vector.transpose()
            theta = speed * (time/ TR)
            theta = (math.pi / 180) * theta
            XY = np.matrix([[np.cos(theta),-np.sin(theta),0], [np.sin(theta), np.cos(theta),0],[0, 0, 1]])
            XY = np.dot(XY,vector)
            XY = XY.transpose()
            return np.matrix(XY) 


def DecayRecoveryEquation(T1,T2,PD,vector,time):
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


def ernstAngleFun():
        vector= np.dot (130,np.matrix ([0,0,1])) 
        intensity = np.zeros(18)
        j =0
        for theta in range ( 0, 190 , 10):
            
            for i in range(10):
                vector = rotationAroundYaxisMatrix(theta,vector)
                vector = DecayRecoveryEquation(2600,50,1,vector,1000)
            
            intensity[j] = math.sqrt((vector[0]^2)+(vector[1]^2))
            j+=1
        


ernstAngleFun()


def decayEquation(T1,T2,PD,vector,time):
            vector = vector.transpose()
            Decay =np.matrix([[np.exp(-time/T2),0,0],[0,np.exp(-time/T2),0],[0,0,1]])
            Decay = np.dot(Decay,vector)
            Decay = np.transpose(np.matrix(Decay))
            return Decay


vector= np.matrix ([2,3,1])  
print(vector)
vector=decayEquation(100,20,1,vector,1)
print(vector)
print(type(vector))
print(vector.shape)


size = 9
signal = [[[0 for k in range(3)] for j in range(size)] for i in range(size)]
phantom = phantom(n=9)
plt.imshow(phantom, cmap="gray")
plt.show()
print(signal)
for i in range(size):
        for j in range(size):
            signal[i][j][1]=phantom[i][j]

print(signal)

t2 = np.array([150, 120,50,170,200])
myT2Range =  np.array([min(t2), max(t2)+20])
intensity =np.array([0, 255])
t2 = np.interp(t2,myT2Range,intensity)

print(t2)

t1 = np.array([1000, 1200,1300,1500,2000])
myT1Range =  np.array([min(t1), max(t1)+20])
intensity = np.array([0, 255])
t1 = np.interp(t1,myT1Range,intensity)

print(t1)


if self.scale[i][j]>=0 and self.scale[i][j]<=50:
                       self.t1[i][j]=10000
                       self.t2[i][j]=10
                   elif self.scale[i][j]<=100 and self.scale[i][j] >=50:
                       self.t1[i][j]=1700
                       self.t2[i][j]=150
                   elif self.scale[i][j] <=150 and self.scale[i][j] >=100 :
                        self.t1[i,j]=2600
                        self.t2[i,j]=50
                   elif self.scale[i,j] <=200 and self.scale[i,j] >=150:
                        self.t1[i,j]=3900
                        self.t2[i,j]=200
                   elif self.scale[i,j] <=255 and self.scale[i,j] >=200:
                        self.t1[i,j]=6000
                        self.t2[i,j]=250
                   else:
                        break 

                           if self.scale[i][j]>=0 and self.scale[i][j]<=50 :
                               self.t1[i][j]=1000
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
                        """


def mappingToIntensity(array):
        maxx = np.max(array)
        minn = np.min(array) 
        array = (((255-2)/(maxx-minn))*(array-minn+2))
        return array

t2 = np.array([150, 120,50,170,200])
t1 = np.array([1000, 1200,1300,1500,2000])

print(mappingToIntensity(t2))

print(mappingToIntensity(t1))
    