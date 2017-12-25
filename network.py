'''
Created on 2017/12/25

@author: fukemasashi
'''
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation    
from keras.wrappers.scikit_learn import KerasClassifier

model = Sequential()
model.add(Dense(50,input_shape=(64,)))
model.add(Activation('relu'))
    
model.add(Dense(100))
model.add(Activation('relu'))
    
model.add(Dense(64))
model.add(Activation('softmax'))
    
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(),
    metrics=['accuracy'])
    
def compstone(X_train,Y_train):
    model.fit(X_train,Y_train)
    hdf5_file = './riversi-model.hdf5'
    model.save_weights(hdf5_file)
    res = model.predict(X_train,Y_train)
    return [res % 8, res // 8]
    