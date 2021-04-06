#!/usr/bin/python
import sys
import datetime
from logFiles import createLogs
from constants import constants
from cloud import cloudManagment

writelogfile = createLogs.createLogs()
cm = cloudManagment.firebaseManagment(constants.FIREBASE_URL)
cm.getNewRecordings()
