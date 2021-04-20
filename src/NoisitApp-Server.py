#!/usr/bin/python
import sys
import datetime
from logFiles import createLogs
from constants import constants
from cloud import cloudManagment
from readFiles import readFiles

index = 0

rf = readFiles.readFiles()
classificationLabels = rf.getArrayFromFile(constants.ARRAYPATH)
writelogfile = createLogs.createLogs()
cm = cloudManagment.firebaseManagment(constants.FIREBASE_URL)
if (cm.existNewRecordings()):
    recordings,paths = cm.getRecordingsNameAndPath()
    for record in recordings:
        user_mail = cm.getUser(paths[index])
        print(constants.AUDIOPROCESSEDSTRING + record + constants.USERFROMAUDIO + user_mail)
        print(constants.DOWNLOADING_STRING)
        cm.downLoadFiletoFolder(record,constants.FIRESTORE_PATH+record)
        print(constants.DOWNLOADED_STRING)
        print(constants.DELETING_STRING)
        #rf.deleteFile(constants.FIRESTORE_PATH+record)
        print(constants.DELETED_STRING)
        #writelogfile.printWarning(record)
    #Donothing
    