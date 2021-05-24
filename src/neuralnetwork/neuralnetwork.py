import os
import numpy as np
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics 
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical
import librosa
from IPython import display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
    
class NeuralNetwork():
    def __init__(self,commands):
        self.commands=commands
    def modelExists(self,model_path):
        #miramos si esta emtrenado el 
        return os.path.isfile(model_path)
    def predictLabel(self,file_path,model_path):
        # Cargamos el modelo entrenado
        # descargamos 
        if(self.modelExists(model_path+'theModel.h5')):
            labelencoder = LabelEncoder()
            model = load_model(model_path+'theModel.h5')
            #Obtenemos el label encoder programada
            labelencoder.classes_ = np.load(model_path+'classes.npy')
            librosa_audio_data,librosa_sample_rate = librosa.load(file_path,sr=1600)
            mfccs = librosa.feature.mfcc(y=librosa_audio_data, sr=librosa_sample_rate, n_mfcc=40)
            mfccs_scaled_features = np.mean(mfccs.T,axis=0)
            mfccs_scaled_features=mfccs_scaled_features.reshape(1,-1)
            predicted_label=model.predict_classes(mfccs_scaled_features)
            prediction_class = labelencoder.inverse_transform(predicted_label)
            #obtenemos el resultado
            return prediction_class[0]
        else:
            return "Needs To train the model"
