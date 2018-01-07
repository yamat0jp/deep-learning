'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation,Flatten,Reshape
from keras.layers import InputLayer,Conv2D,LSTM,MaxPooling2D,GRU
from keras.layers.embeddings import Embedding
import numpy as np
import os

class  Comp():
    def __init__(self):
        self.filename = 'sente-hyouka.hdf5'
        
        self.model1,self.model2 = self.model(),self.model()
        
        self.hyouka = Sequential()

        self.hyouka.add(InputLayer(input_shape=(8,8,60)))
        self.hyouka.add(Conv2D(10,(4,4)))
        self.hyouka.add(Activation('relu'))
        
        self.hyouka.add(Conv2D(10,(4,4)))
        self.hyouka.add(Activation('relu'))
        
        self.hyouka.add(MaxPooling2D(pool_size=(2,2)))
        self.hyouka.add(Flatten())
            
        #self.hyouka.add(GRU(60,input_shape=(60,60))) 
        self.hyouka.add(Activation('softmax'))
    
        self.hyouka.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])

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
    
    def hyouka(self,X,Y):
        X,Y = np.array(X),np.array(Y)
        X = np.reshape(np.float32(X),(-1,8,8,60))  
        if os.path.exists:
            self.hyouka.load_weights(self.filename)
        self.hyouka.fit(X,Y)
        self.hyouka.save_weights(self.filename)
        
    def calscore(self,result,X):
        s = [0 for x in range(len(result))]
        for x in range(len(result)):
            i,j = x//8,x%8
            if result[x] != 0:
                X[i][j] = 1
                s[x] = self.hyouka.predict(np.array(X))#8,8
                X[i][j] = 0
            else:
                s[x] = 0
        return s
    
    def sente_stone(self,X_train,Y_train,train):
        hdf5_file = 'sente-model.hdf5'
        if os.path.exists(hdf5_file):
            self.model1.load_weights(hdf5_file)
        if os.path.exists(self.filename):
            self.hyouka.load_weights(self.filename)
        X,Y = np.array(X_train),np.array(Y_train)        
        X = np.reshape(np.float32(X),(1,64))
        Y = np.reshape(np.float32(Y),(1,64))
        if train:
            self.model1.fit(X,Y)
        res = self.model1.predict(X)
        scores = self.calscore(res[0],X_train)  
        res = (res + np.array(scores) ) / 2
        while True:
            s = np.argmax(res)
            if res[0][s] == 0:
                s = np.argmax(Y)
            elif Y[0][s] == 0:
                res[0][s] = 0
                continue
            break
        if train:
            self.model1.save_weights(hdf5_file)
        return [s // 8, s % 8]
        
    def gote_stone(self,X_train,Y_train,train):
        hdf5_file = 'gote-model.hdf5'
        if os.path.exists(hdf5_file):
            self.model2.load_weights(hdf5_file) 
        X,Y = np.array(X_train),np.array(Y_train)
        X = np.reshape(np.float32(X),(1,64))
        Y = np.reshape(np.float32(Y),(1,64))
        if train:
            self.model2.fit(X,Y)
        res = self.model2.predict(X)
        while True:
            s = np.argmax(res)
            if res[0][s] == 0:
                s = np.argmax(Y)
            elif Y[0][s] == 0:
                res[0][s] = 0
                continue
            break
        self.model2.save_weights(hdf5_file)
        return [s // 8, s % 8]
