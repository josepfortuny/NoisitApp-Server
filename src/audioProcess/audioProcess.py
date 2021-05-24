# Importing the Keras libraries and packages
import os
from numpy import pi, polymul,convolve,mean
from scipy.fftpack import fft
from scipy.signal import bilinear
from scipy.signal import lfilter,freqz
from scipy.io import wavfile
import matplotlib.pyplot as plt
from numpy import inf
import numpy as np
import pydub 
import math
"""
Note that this uses a bilinear transform and so is not accurate at high frequencies.
Apply an A-weighting filter to a sound stored as a NumPy array.
"""

class audioProcessing():
    def __init__(self,plotenable):
        self.cal_factor= 20 # factor de calibracio
        self.plotenable=plotenable
        
    def A_weighting(self,fs):
        # Definicion del A-weighting filtro segun IEC/CD 1672
        
        f1 = 20.598997
        f2 = 107.65265
        f3 = 737.86223
        f4 = 12194.217
        A1000 = 1.9997

        NUMs = [(2 * pi * f4)**2 * (10**(A1000/20)), 0, 0, 0, 0]


        DENs = convolve([1, 4 * pi * f4, (2 * pi * f4)**2], 
                            [1, 4 * pi * f1, (2 * pi * f1)**2])

        DENs = convolve(convolve(DENs, [1, 2 * pi * f3]), 
                                     [1, 2 * pi * f2])
        return bilinear(NUMs,DENs,fs)
    
    def mp4_to_wav(self,path):
        # Convertir de mp4 a wav 
        audio = pydub.AudioSegment.from_file(path, format="mp4")
        audio.export("audio.wav", format="wav")
    def rms_flat(self,a):  
        """
        Return the root mean square of all the elements of *a*, flattened out.
        """
        return np.sqrt(np.mean(np.absolute(a)**2))
        
        
    def calculateLEQfromAudio(self,path):
        self.mp4_to_wav(path)
        fs,audio=wavfile.read("audio.wav")
        # Ponderacion del A filter
        B,A = self.A_weighting(fs) 
        T = 1
        L = round(T*fs)
        y = lfilter(B,A,audio)
        third_factor= abs(y)**2.
        ones = np.ones(L)
        befDB=((1/L)*lfilter(ones,1,third_factor))
        ym = 10*np.log10(befDB[:-1]) + self.cal_factor
        LAeq = ym[1::L]
        LAeq [ LAeq == -inf ] = 0.0
        LAeq [ LAeq == inf ] = 0.0
        # si se quiere debugar y se quiere mostrar la respuesta frequencial
        if (self.plotenable):
            t=np.zeros(len(audio))
            i=0
            print(len(audio))
            for i in range(len(audio)):
                t[i]=(i/fs) 
            fig,axs = plt.subplots(2)
            axs[0].set_title('senyal daudio original')
            axs[0].set(xlabel='semps (seg.)',ylabel='amplitud')
            axs[0].set_xscale('log') 
            axs[0].plot(t,audio)
            axs[1].set_title('Senyal amb ponderacio A')
            axs[1].set(xlabel='semps (seg.)',ylabel='amplitud')
            axs[1].set_xscale('log')  
            axs[1].plot(t,y)
            """axs[2].set_title('Nivell equivalent amb ponderacio A')
            axs[2].set(xlabel='semps (seg.)',ylabel='amplitud') 
            axs[2].plot([1::L],LAeq)"""
            plt.show()
        return LAeq
