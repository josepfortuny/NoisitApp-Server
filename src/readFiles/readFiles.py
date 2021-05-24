import os
import numpy as np
class readFiles():
    def __init__(self):
        #Do nothing
        self.donothing=""
    def getArrayFromFile(self,path):
        #Obtencion de los comandos a parti del fichero
        arrayTags =[]
        with open(path,'r+') as filehandler:
            for line in filehandler:
                arrayTags.append(line[:-1])
        return np.array(arrayTags)
    def deleteFile(self,path):
        if (os.path.exists(path)):
            os.remove(path)
            