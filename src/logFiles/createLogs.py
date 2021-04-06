#importing module
import logging

class createLogs():
    def __init__(self):
        #Create and configure logger
        logging.basicConfig(filename="logFiles/log_file.log",
                            format='%(asctime)s %(message)s',
                            level=logging.INFO,
                            filemode='w')


    def printWarning(self,message):
        logging.warning(" Warning  "+ message)
    def printError(self,message):
        logging.error(" Error  "+ message)
    def printCritical(self,message):
        logging.critical(" Critical  "+ message)