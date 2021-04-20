#importing module
import logging
import time

class createLogs():
    def __init__(self):
        #Create and configure logger
        logging.basicConfig(filename="logFiles/log_file.log",
                            format='%(asctime)s %(message)s',
                            level=logging.INFO,
                            filemode='w')


    def printWarning(self,message):
        
        logging.warning(": Warning  "+ message)
    def printError(self,message):
        # Current Day
        Day = time.strftime("%m-%d-%Y", time.localtime())
        # Current Time
        Time = time.strftime("%I:%M:%S %p", time.localtime())
        logging.error(Day + Time +": Error  "+ message)
    def printCritical(self,message):
        # Current Day
        Day = time.strftime("%m-%d-%Y", time.localtime())
        # Current Time
        Time = time.strftime("%I:%M:%S %p", time.localtime())
        logging.critical(Day + Time +": Critical  "+ message)