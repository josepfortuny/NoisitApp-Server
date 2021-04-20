from firebase import firebase
from constants import constants
from pyrebase import pyrebase


class firebaseManagment():
    def __init__ (self,url):
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
        users = self.db.get(constants.USERS_FIREBASE_PATH,None)
        index = 0
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
        decode_data = path.split('/')
        user_previous_path = "/"+decode_data[1]+"/"+decode_data[2]+"/"
        user = self.db.get(user_previous_path,None)
        return user["email"]
    
    def downLoadFiletoFolder(self,file,downloadpath):
        self.firebase_storage.child(file).download(downloadpath)
        #self.firebase_storage.child(downloadpath).download(file)
    """
            self.days.append(aux_day)
    def print_planned_pills(self,day):
        print("Today is : ",self.days[day].day)
        if (len(self.days[day].pills) > 0):
            print ("Your planned pills for today are:")
            for pill in self.days[day].pills:
                print (pill.pillName)
            return True
        else:
            print ("There are no pills planned for today")
            return False
    def print_calendar(self):
        print("Week Calendar:")
        for i in range(7):
            print (self.days[i].day,":")
            if (len(self.days[i].pills) > 0):
                print ("Your planned pills for", self.days[i].day + " are :")
            for pill in self.days[i].pills:
                print (pill.pillName)
            else:
                print ("There are no pills planned for ", self.days[i].day)
    def is_pill_planned(self,pill_predicted,current_day):
        for pill in self.days[current_day].pills:
            if( pill.pillName == pill_predicted ):
                return True
        return False
    def next_day(self,day):
        if (day < 6):
            day +=1
        else:
            day =0
        return day
    def post_pill_taken(self, day,pill_predicted):
        i =0
        for pill in self.days[day].pills:
            if( pill.pillName == pill_predicted ):
                now = datetime.datetime.now()
                self.days[day].pills[i].pillTaken=True
                self.days[day].pills[i].date = str(now.hour)+":"+str(now.minute)
                write_path = self.calendar_path+"/"+str(day)+"/pills/"+str(i)+"/"
                #print(write_path)
                self.db.put(write_path, "date",self.days[day].pills[i].date)
                self.db.put(write_path, "pillTaken",True)"""