'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation    
import numpy as np
import os

class  Comp():
    def __init__(self):
        self.model1,self.model2 = Sequential(),Sequential()

        self.model1.add(Dense(50,input_shape=(64,)))
        self.model1.add(Activation('relu'))
    
        self.model1.add(Dense(100))
        self.model1.add(Activation('relu'))
    
        self.model1.add(Dense(64))
        self.model1.add(Activation('softmax'))
    
        self.model1.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])

        self.model2.add(Dense(50,input_shape=(64,)))
        self.model2.add(Activation('relu'))
        self.model2.add(Dense(64))    
        self.model2.add(Activation('softmax'))
        self.model2.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy'])
        
        
        s = 'sente-model.hdf5'
        if os.path.exists(s):
            self.model1.load_weights(s)
        s = 'gote-model.hdf5'
        if os.path.exists(s):
            self.model2.load_weights(s)
        
    def sente_stone(self,X_train,Y_train):
        X,Y = np.array(X_train),np.array(Y_train) 
        X = np.reshape(X,[1,64])
        Y = np.reshape(Y,[1,64])
        self.model1.fit(X,Y)
        hdf5_file = './sente-model.hdf5'
        self.model1.save_weights(hdf5_file)
        res = self.model1.predict(X,1)
        i = np.argmax(res)
        print(res,i)
        return [i % 8, i // 8]
        
    def gote_stone(self,X_train,Y_train):
        X,Y=np.array(X_train),np.array(Y_train)
        X = np.reshape(X,[1,64])
        Y = np.reshape(Y,[1,64])
        self.model2.fit(X,Y)
        hdf5_file ='./gote-model.hdf5'
        self.model2.save_weights(hdf5_file)
        res = self.model2.predict(X,1)
        i = np.argmax(res)
        return [i % 8, i // 8]
