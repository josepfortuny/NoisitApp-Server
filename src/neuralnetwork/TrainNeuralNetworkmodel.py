import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics 
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import tensorflow as tf
import tensorflow_hub as hub

from keras.callbacks import ModelCheckpoint 
from sklearn.model_selection import train_test_split 
import pandas as pd
import random
import os
import librosa
import glob

#Lista de comandos a entrenar segun los datasets
commands= np.array(['airport' ,'bus' ,'metro_station' ,'park' ,'public_square' ,'shopping_mall','street_pedestrian', 'tram'])
#Label Encoder es 
labelencoder=LabelEncoder()
#Usaremos los Mel-Frequency Cepstral Coefficients(MFCC) de las muestras de audio
#Las MFCC resume la distribucion de frequencia para que sea analizable por freqnuencia y tiempo.
#Indispensables para la classificaión

def extract_features(file_name):
    librosa_audio_data,librosa_sample_rate = librosa.load(file_name,sr=1600)
    mfccs = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs.T,axis=0)
    return mfccs_scaled_features
#Obtencion de los datos y el label del training ser
def get_labels_data(filenames):
    features = []
    labels = []
    for file in filenames :
        data = extract_features(file)
        labels = file.split('-')
        labels = labels[0].split('/')
        features.append([data,labels[2]])
    return features

"""
Construiremos un modelo de red neuronal, concretamente utilizaremos una red neuronal convolucional.

Las redes neuronales convolucionales funcionan muy bien para la clasificación de imágenes, debido a la extracción de características y partes a clasificar.

Viendo el comportamiento de MFCC, observamos que se puede extrapolar al comportamiento que tienen estas redes en imágenes.

Para su implementación, utilizaremos un modelo secuencial, comenzando con una arquitectura de modelo simple, que consta de cuatro capas de convolución Conv2D con sus capas de poolling, siendo nuestra capa de salida final una capa densa.

Las capas de convolución están diseñadas para la detección de características. Funciona deslizando una ventana de filtro filter sobre la entrada y realizando una multiplicación de matriz y almacenando el resultado en un mapa de características. Esta operación se conoce como convolución.

El parámetro de filtro especifica el número de nodos en cada capa. Cada capa aumentará de tamaño de 16, 32, 64 a 128, mientras que el parámetro kernel_size especifica el tamaño de la ventana del kernel, que en este caso es 2, lo que da como resultado una matriz de filtro 2×2.

La primera capa recibirá la forma de entrada de (40, 174, 1) donde 40 es el número de MFCC, 174 es el número de cuadros que tienen en cuenta el relleno y el 1 significa que el audio es mono.

La función de activación que utilizaremos para nuestras capas convolucionales es ReLU.

También destacar que aplicaremos un Dropout del 20%. Esto excluirá al azar los nodos de cada ciclo de actualización, lo que a su vez da como resultado una red que es capaz de responder mejor a la generalización y es menos probable que se produzca sobreajuste en los datos de entrenamiento.

Cada capa convolucional tiene una capa de agrupación asociada de tipo MaxPooling2D con la capa convolucional final que tiene un tipo GlobalAveragePooling2D. La capa de agrupación reduce la dimensionalidad del modelo (al reducir los parámetros y los requisitos de cálculo subsiguientes), lo que sirve para acortar el tiempo de entrenamiento y reducir el sobreajuste. El tipo de agrupación máxima toma el tamaño máximo para cada ventana y el tipo de agrupación promedio global toma el promedio que es adecuado para alimentar nuestra capa de salida densa.

Finalmente la capa de salida tendrá 10 nodos, que coinciden con el número de clasificaciones posibles. La activación es para nuestra capa de salida la función softmax. Softmax hace que la salida sume 1, por lo que la salida puede interpretarse como probabilidades. El modelo hará su predicción según la opción que tenga la mayor probabilidad.
"""

def create_Model(x_train,y_train,x_test,y_test):
    num_rows = 40
    num_columns = 174
    num_channels = 1
    num_labels = y_train.shape[1]
    num_epochs = 140
    num_batch_size = 100
    
    # Construct model 
    
    model=Sequential()
    ###first layer
    model.add(Dense(100,input_shape=(40,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    ###second layer
    model.add(Dense(200))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    ###third layer
    model.add(Dense(100))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    ###final layer
    model.add(Dense(num_labels))
    model.add(Activation('softmax'))
    model.summary()
    """Compilar el modelo
    Para compilar nuestro modelo, utilizaremos los siguientes tres parámetros:

    Función de pérdida: utilizaremos categorical_crossentropy. Esta es la opción más común para la clasificación. Una puntuación más baja indica que el modelo está funcionando mejor.
    Métricas: utilizaremos la métrica de accuracy que nos permitirá ver la precisión en los datos de validación cuando entrenemos el modelo.
    Optimizador: aquí usaremos adam, que generalmente es un buen optimizador para muchos casos de uso.
    """
    # Compile the model
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam') 
    
    model.summary()
        
    checkpointer = ModelCheckpoint(filepath='saved_models/weights.best.basic_cnn.hdf5', 
                               verbose=1, save_best_only=True)
    
    
    model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)
    
    model.save('theModel.h5')
    
def train():
    features = []
    # listar todos los filenames
    filenames = glob.glob('datasets/*/*')
    
    features = get_labels_data(filenames)
    # Convertir los datos a panda
    featuresdf = pd.DataFrame(features, columns=['feature','class_label'])
    #Convertir los datos y etiquetas
    #Para transformar los datos categóricos a numéricos, usaremos LabelEncoder
    #y así conseguiremos que el modelo sea capaz de entenderlos.
    # Convert features and corresponding classification labels into numpy arrays
    X = np.array(featuresdf.feature.tolist())
    
    Y = np.array(featuresdf.class_label.tolist())
    
    # codificar los labels
    
    y = to_categorical(labelencoder.fit_transform(Y))
    np.save('classes.npy', labelencoder.classes_)
    #Dividir los datos en entrenamiento y test¶
    #Dividimos el conjunto de datos en dos bloques (80% y 20%) y de ellos sacamos valores de X y de Y.

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)
    
    create_Model(x_train, y_train,x_test,y_test)

train()
