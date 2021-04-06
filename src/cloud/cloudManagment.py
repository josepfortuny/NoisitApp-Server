from firebase import firebase



class firebaseManagment():
    def __init__ (self,url):
        self.db = firebase.FirebaseApplication(url,None)
        
    
    def getNewRecordings(self):
        users = self.db.get('/Users',None)
        new_records =[]
        for user in users:
            user_info = self.db.get('/Users',user )
            record_info = self.db.get('/Users/'+user+'/records',None)
            if (record_info is not None):
                for recording in record_info:
                    # falta condició de si sha obtingut o no
                    new_records.append(recording["path"])
        print(new_records)    
        return new_records        
                
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