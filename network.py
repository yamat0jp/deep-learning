'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation
from keras.layers import InputLayer,Conv2D,LSTM,MaxPooling2D
import numpy as np
import os

class  Comp():
    def __init__(self):
        self.model1,self.model2 = self.model(),self.model()
        
        self.hyouka = Sequential()

        self.hyouka.add(InputLayer(input_shape=(8,8,60)))
        self.hyouka.add(Conv2D(1,(4,4)))
        self.hyouka.add(Activation('relu'))
        
        self.hyouka.add(LSTM(60,input_shape=(None,5,5,60)))    
    
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
        self.hyouka.fit(X,Y)
        
    def calscore(self,result,X):
        for x in range(len(result)):
            i,j = x//8,x%8
            if result[x] != 0:
                X[i][j] = 1
                yield self.hyouka.predict(X)
                X[i][j] = 0
            else:
                yield 0
    
    def sente_stone(self,X_train,Y_train,train):
        hdf5_file = 'sente-model.hdf5'
        filename = 'sente-hyouka.hdf5'
        if os.path.exists(hdf5_file):
            self.model1.load_weights(hdf5_file)
        if os.path.exists(filename):
            self.hyouka.load_weights(filename)
        X,Y = np.array(X_train),np.array(Y_train)
        X = np.reshape(np.float32(X),(1,64))
        Y = np.reshape(np.float32(Y),(1,64))
        if train:
            self.model1.fit(X,Y)
        res = self.model1.predict(X)
        scores = self.calscore(res[0],X_train)
        res = (res + np.array(np.float32(scores)) ) / 2
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
