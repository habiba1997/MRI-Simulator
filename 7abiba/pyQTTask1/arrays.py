from array import *
import numpy as np
 
#Create a DataFrame

T = [[1, 2, 3, 4], [5, 6, 7,8], [9, 10, 11, 12], [13,14,15,16]]
T = np.array(T)
m2loba = np.fliplr(T)



m2loba[:,0:2] =0

T = np.fliplr(m2loba)


#T[:, -3:-1] = 0
