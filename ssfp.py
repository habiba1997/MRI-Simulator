def SSFPForLoops(self):    
        angle60 = True

        for i in range(self.size):
            for j in range(self.size):
                self.signal[i][j] =  self.rotationAroundYaxisMatrix((self.f/2),np.matrix(self.signal[i][j]))
                self.signal[i][j] = self.DecayRecoveryEquation(self.t1[i][j],self.t2[i][j],1,np.matrix(self.signal[i][j]),self.tr)
            
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
                        self.signal[i][j] = np.dot (self.signal[i][j], np.exp(-self.te/self.t2[i][j]))


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