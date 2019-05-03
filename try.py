import numpy as np
from shapeloggin import phantom 
from matplotlib import pyplot as plt

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


""""
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


t2 = np.array([100,100, 120,150,170,200])
myT2Range =  np.array([min(t2), max(t2)+25])
intensity =np.ravel(signal[i][j])[2] np.array([0, 255])
t2 = np.interp(t2,myT2Range,intensity)

print(t2)

t1 = np.array([1000, 1200,1300,1500,2000])
myT1Range =  np.array([min(t1), max(t1)+25])
intensity = np.array([0, 255])
t1 = np.interp(t1,myT1Range,intensity)

print(t2)"""