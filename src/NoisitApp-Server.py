#!/usr/bin/python
import sys
import datetime
from logFiles import createLogs
from constants import constants
from cloud import cloudManagment
from readFiles import readFiles
from neuralnetwork import neuralnetwork
from audioProcess import audioProcess
from neuralnetwork import neuralnetwork
#Inicializamos las classes
index = 0
ap = audioProcess.audioProcessing(False)
rf = readFiles.readFiles()
classificationLabels = rf.getArrayFromFile(constants.ARRAYPATH)
nn=neuralnetwork.NeuralNetwork(classificationLabels)
writelogfile = createLogs.createLogs(constants.LOG_PATH)
cm = cloudManagment.firebaseManagment(constants.FIREBASE_URL)
#comprobamos si existe un proceso nuevo
#grabamos los pasos en el fichero log
if (cm.existNewRecordings()):
    #Obtencion de los recordings sin classificar
    recordings,paths = cm.getRecordingsNameAndPath()
    # Lo separamos individualmente
    for record in recordings:
        # Obtenemos el usuario del record
        user_mail = cm.getUser(paths[index])
        writelogfile.printing(constants.AUDIOPROCESSEDSTRING + record + constants.USERFROMAUDIO + user_mail)
        writelogfile.printing(constants.DOWNLOADING_STRING)
        # Descargamos el fichero
        cm.downLoadFiletoFolder(record,constants.FIRESTORE_PATH+record)
        # Calculamos LAEQ
        writelogfile.printing(constants.DOWNLOADED_STRING)
        laeq =ap.calculateLEQfromAudio(constants.FIRESTORE_PATH+record)
        #Calculamos la prediccion y la escubimos en firebase
        cm.writeRecordData(nn.predictLabel(constants.FIRESTORE_PATH+record,constants.MODEL_PATH),laeq,paths[index])
        writelogfile.printing(constants.DELETING_STRING)
        #Eliminamos el fichero
        rf.deleteFile(constants.FIRESTORE_PATH+record)
        writelogfile.printing(constants.DELETED_STRING)
        index += 1
