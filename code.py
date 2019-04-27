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
             for j in range (self.size):
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