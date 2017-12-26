'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation    
import numpy as np

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

    def sente_stone(self,X_train,Y_train):
        X,Y = np.array(X_train),np.array(Y_train) 
        X = np.reshape(X,[],1)
        Y = np.reshape(Y,[],1)
        self.model1.fit(X,Y)
        hdf5_file = './sente-model.hdf5'
        #self.model1.save_weights(hdf5_file)
        res = self.model1.predict(X,Y)
        i = 0
        for j in res:
            if j != 0:
                return [i % 8, i // 8]
            i += 1

    def gote_stone(self,X_train,Y_train):
        X,Y=np.array(X_train),np.array(Y_train)
        X = np.reshape(X,0,[])
        Y = np.reshape(Y,0,[])
        self.model2.fit(X,Y)
        hdf5_file ='./gote-model.hdf5'
        #self.model2.save_weights(hdf5_file)
        res = self.model2.predict(X,Y)
        i = 0
        for j in res:
            if j != 0:
                return [i % 8, i // 8]
            i += 1
