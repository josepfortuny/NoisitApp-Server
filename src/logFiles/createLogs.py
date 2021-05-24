#importing module
import logging
import time

class createLogs():
    def __init__(self,path):
        #Create and configure logger
        logging.basicConfig(filename=path+"logFiles/log_file.log",
                            format='%(asctime)s %(message)s',
                            level=logging.INFO,
                            filemode='w')

    def printing(self,message):
        logging.info(message)
    def printWarning(self,message):
        logging.warning(": Warning  "+ message)
    def printError(self,message):
        logging.error(Day + Time +": Error  "+ message)
    def printCritical(self,message):
        logging.critical(Day + Time +": Critical  "+ message)