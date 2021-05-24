from firebase import firebase
from constants import constants
from pyrebase import pyrebase


class firebaseManagment():
    def __init__ (self,url):
        #Inicializacion configuracion de firebase
        firebaseConfigfirebaseConfig = {
            'apiKey': "AIzaSyCjg37v8Kf75RTi4O9KO5gcKG7MmVyaamA",
            'authDomain': "lasalleacousticapp.firebaseapp.com",
            'databaseURL': "https://lasalleacousticapp.firebaseio.com",
            'projectId': "lasalleacousticapp",
            'storageBucket': "lasalleacousticapp.appspot.com",
            'messagingSenderId': "471079503444",
            'appId': "1:471079503444:web:b29ff5157e45b476eb0fc1"}
        firebase_app= pyrebase.initialize_app(firebaseConfigfirebaseConfig)
        self.firebase_storage = firebase_app.storage()
        self.db = firebase.FirebaseApplication(url,None)
        self.new_records_path =[]
        self.new_records_name =[]
        
    def getRecordingsNameAndPath(self):
        return self.new_records_name,self.new_records_path
    
    def existNewRecordings(self):
        #hace un check para ver si hay alguna grabación sin el machineLearningApplied
        # en caso positivo se guard el estado y se obtiene el path de la grabacion
        index = 0
        users = self.db.get(constants.USERS_FIREBASE_PATH,None)
        isPendingRecording = False
        for user in users:
            user_info = self.db.get(constants.USERS_FIREBASE_PATH,user)
            record_info = self.db.get(constants.USERS_FIREBASE_PATH+user+constants.RECORDS_FIREBASE_PATH,None)
            if (record_info is not None):
                for recording in record_info:
                    if (recording["machineLearningApplied"] == False):
                        self.new_records_name.append(recording["path"])
                        self.new_records_path.append(constants.USERS_FIREBASE_PATH+user+constants.RECORDS_FIREBASE_PATH+str(index)+'/')
                        isPendingRecording = True
                    index += 1
        return isPendingRecording
    
    def getUser(self,path):
        #Obtememos el gmail del usuario
        decode_data = path.split('/')
        user_previous_path = "/"+decode_data[1]+"/"+decode_data[2]+"/"
        user = self.db.get(user_previous_path,None)
        return user["email"]
    
    def downLoadFiletoFolder(self,file,downloadpath):
        print(downloadpath)
        #Descargamos el fichero
        self.firebase_storage.child(file).download(downloadpath)
        
    def writeRecordData(self,tagApplied,laeqData,path):
        # Escribimos los datos de 
        self.db.put(path,"Laeq",laeqData.tolist())
        self.db.put(path,"iaGeneratedLabel",tagApplied)
        self.db.put(path,"machineLearningApplied",True)
