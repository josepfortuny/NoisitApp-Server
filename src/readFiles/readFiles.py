import os
class readFiles():
    def __init__(self):
        #Do nothing
        self.donothing=""
    def getArrayFromFile(self,path):
        arrayTags =[]
        with open(path,'r+') as filehandler:
            for line in filehandler:
                arrayTags.append(line[:-1])
        return arrayTags
    def deleteFile(self,path):
        if (os.path.exists(path)):
            os.remove(path)
            