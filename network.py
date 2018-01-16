'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Activation,Flatten,Dropout
from keras.layers import InputLayer,Conv2D
import numpy as np
import os

class  Comp():
    def __init__(self):
        self.filename = 'sente-hyouka.hdf5'
        
        self.model1,self.model2 = self.model(),self.model()
        
        self.hyouka = Sequential()

        self.hyouka.add(InputLayer(input_shape=(8,8,5)))
        self.hyouka.add(Conv2D(5,(4,4)))
        self.hyouka.add(Activation('relu'))
        
        self.hyouka.add(Conv2D(5,(4,4)))
        self.hyouka.add(Activation('relu'))
        self.hyouka.add(Flatten())
        
        self.hyouka.add(Dense(10))
        self.hyouka.add(Activation('relu'))
        self.hyouka.add(Dense(1))
    
        self.hyouka.compile(
            loss='binary_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])
        
        self.past = []

    def model(self):
        model = Sequential()
        model.add(Dense(100,input_shape=(64,)))
        model.add(Activation('sigmoid'))
        model.add(Dropout(0.25))
        model.add(Dense(100))
        model.add(Activation('sigmoid'))
        model.add(Dropout(0.25))
        model.add(Dense(64))    
        model.add(Activation('softmax'))
        model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])
        return model
    
    def gakushu(self,Y):
        if len(self.past) < 5:
            return
        temp = self.past[len(self.past)-1]
        s = True
        k = 0
        for i in range(8):
            for j in range(8):
                if temp[i][j] == 0:
                    s = False
                    break
                elif temp[i][j] == 1:
                    k += 1                        
            if s == False:
                break
        if s == True:
            if k > 32:
                Y += 10
            else:
                Y -= 10
        X,Y = np.array(self.past),np.array(Y)
        X = np.reshape(np.float32(self.past),(-1,8,8,5))
        Y = np.reshape(Y,(1,1))
        self.hyouka.fit(X,Y)
        
    def calscore(self,X,result):
        from reversi import GetBanmen
        if len(self.past) < 5:
            return None
        s = []     
        for i in range(8):
            for j in range(8):
                if result[i][j] == 0:
                    s.append(0)
                    continue
                k = GetBanmen(X,(i,j))
                if k == None:
                    s.append(0)
                    continue
                if len(self.past) == 5:
                    temp = self.past[0]
                    self.past.pop(0)
                self.past.append(k)
                t = self.hyouka.predict(np.reshape(np.float32(self.past),(-1,8,8,5)))
                s.append(t[0])
                self.past.pop(len(self.past)-1)
                self.past.insert(0,temp)
        return s
    
    def sente_stone(self,X_train,Y_train,Z):
        hdf5_file = 'sente-model.hdf5'
        if os.path.exists(hdf5_file):
            self.model1.load_weights(hdf5_file)
        if os.path.exists(self.filename):
            self.hyouka.load_weights(self.filename)
        X,Y = np.array(X_train),np.array(Y_train)
        if len(self.past) == 5:
            self.past.pop(0)
        self.past.append(X)        
        X = np.reshape(np.float32(X),(1,64))
        Y = np.reshape(np.float32(Y),(1,64))
        self.model1.fit(X,Y)
        res = self.model1.predict(X)
        self.model1.save_weights(hdf5_file)
        self.gakushu(Z)
        scores = self.calscore(X_train,Y_train) 
        self.hyouka.save_weights(self.filename)
        if scores:
            res = (res + np.reshape(np.array(scores),(1,64)) ) / 2
        while True:
            s = np.argmax(res)
            if res[0][s] == 0:
                s = np.argmax(Y)
            elif Y[0][s] == 0:
                res[0][s] = 0
                continue
            break
        return [s // 8, s % 8]
        
    def gote_stone(self,X_train,Y_train):
        hdf5_file = 'gote-model.hdf5'
        if os.path.exists(hdf5_file):
            self.model2.load_weights(hdf5_file) 
        X,Y = np.array(X_train),np.array(Y_train)
        X = np.reshape(np.float32(X),(1,64))
        Y = np.reshape(np.float32(Y),(1,64))
        self.model2.fit(X,Y)
        res = self.model2.predict(X)
        self.model2.save_weights(hdf5_file)
        while True:
            s = np.argmax(res)
            if res[0][s] == 0:
                s = np.argmax(Y)
            elif Y[0][s] == 0:
                res[0][s] = 0
                continue
            break
        return [s // 8, s % 8]
