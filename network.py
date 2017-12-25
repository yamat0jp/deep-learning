'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation    
from keras.wrappers.scikit_learn import KerasClassifier

model1,model2 = Sequential(),Sequential()

model1.add(Dense(50,input_shape=(64,)))
model1.add(Activation('relu'))
    
model1.add(Dense(100))
model1.add(Activation('relu'))
    
model1.add(Dense(64))
model1.add(Activation('softmax'))
    
model1.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

model2.add(Dense(50,input_shape=(64,)))
model2.add(Activation('relu'))
model2.add(Dense(64))    
model2.add(Activation('softmax'))
model2.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])

def sente_stone(X_train,Y_train):
    model1.fit(X_train,Y_train)
    hdf5_file = './sente-model.hdf5'
    model1.save_weights(hdf5_file)
    res = model1.predict(X_train,Y_train)
    return [res % 8, res // 8]

def gote_stone(X_train,Y_train):
    model2.fit(X_train,Y_train)
    hdf5_file ='./gote-model.hdf5'
    model2.save_weights(hdf5_file)
    res = model2.predict(X_train,Y_train)
    return [res % 8, res // 8]
