import pyrebase
from math import radians, cos, sin, asin, sqrt
from twilio.rest import Client
import bitly_api
import time

ttime = time.strftime('%H|%M|%S')
ddate = time.strftime('%d-%m-%Y')

date_time = str(ddate) + "$" + str(ttime)

# Firebase config
config = {
  "apiKey": "######################",
  "authDomain": "minor-proj.firebaseapp.com",
  "databaseURL": "https://minor-proj.firebaseio.com",
  "storageBucket": "minor-proj.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


#Setting up Twilio Messaging Service

account_sid = "######################",  # Twilio Account ID
auth_token  = "######################",     # Twilio Auth Token
client = Client(account_sid, auth_token)


#Haversine Calculation
def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371             # Radius of earth in kilometers
    return c * r

#Nearest Rescue Center Finder Function
def Rescuecenter(rescueid):
    Distance = 9999
    Rescue_Center_Name=""
    Phone_Number=""
    ResData = db.child("Rescue-center").child(rescueid).get()
    for i in ResData.each():
        res_key_id = i.key()
        print(res_key_id)
        a = db.child("Rescue-center").child(rescueid).child(res_key_id).get()
        b = a.val()
        dest_lat = b.get('Location').get('Latitude').encode("ascii")
        dest_lat = float(dest_lat[1:len(dest_lat)-1])
        dest_lon = b.get('Location').get('Longitude').encode("ascii")
        dest_lon = float(dest_lon[1:len(dest_lon)-1])
        dist = haversine(source_lat,source_lon,dest_lat,dest_lon)
        print(dist)
        if haversine(source_lat,source_lon,dest_lat,dest_lon) < Distance :
            Distance = dist
            Rescue_Center_Name = i.key()
            Phone_Number = b.get('Phone number')
            username = b.get('username')
            print username
    
    return (username,Distance, Rescue_Center_Name, Phone_Number)


#Function to send SMS
def Ressendsms() :
    print("Rescue Center Name:",Rescue_Center_Name, "Distance:",Distance,"Kms","Phone Number:",Phone_Number)
    sms_string = "[EMERGENCY] Vehicle No: " + str(Vehicle_No) + "," + "Location: " + str(mod_location_url) + " Image: " + str(mod_image) + " Ph.No.: " + str(Vehicle_Phone)
    print(len(sms_string))
    print(sms_string)
    account_sid = "###############"   # Twilio Account ID
    auth_token  = "###############"     # Twilio Auth Token
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+91 "+Phone_Number, 
        from_="+18652299684",
        body=sms_string
        )

def Clisendsms() :
    sms_string = " Emergency Message sent to Rescue Center. Your issues will be resolved soon. "
    print(len(sms_string))
    print(sms_string)
    account_sid = ""###############""   # Twilio Account ID
    auth_token  = ""###############""     # Twilio Auth Token
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+91 "+Vehicle_Phone, 
        from_="+18652299684",
        body=sms_string
        )


#While Loop which runs continuosly
while True :    
    VehData = db.child("Vehicle_Details").get()
    for i in VehData.each():
        vehid = i.key()
        if vehid != "Dummy Node" :
            a = db.child("Vehicle_Details").child(vehid).get()
            b = a.val()
            source_lat = b.get('Location').get('Latitude').encode("ascii")
            source_lat = float(source_lat[0:len(source_lat)-1])
            source_lon = b.get('Location').get('Longitude').encode("ascii")
            source_lon = float(source_lon[0:len(source_lon)-1])
            print(source_lat,source_lon)
            Vehicle_Phone = int(b.get('Phone Number'))
            Vehicle_Phone = str(Vehicle_Phone)
            print(Vehicle_Phone)
            Image_URL = b.get('Image')[:-1]
            print(Image_URL)
            type = b.get('Type')
            Vehicle_No=b.get('Vehicle Number')
            print(Vehicle_No)

            API_KEY = ""   #API key for bitly
            b = bitly_api.Connection(access_token=API_KEY)
        
            #Image URL Shortening
            longurl = Image_URL
            response = b.shorten(uri=longurl)
            mod_image = str(response.items()[0])[18:32]

            #Location URL Shortening
            locationurl = "https://www.google.com/maps/search/?api=1&query="+str(source_lat)+","+str(source_lon)
            longurl = locationurl
            response = b.shorten(uri=longurl)
            mod_location_url = str(response.items()[0])[11:32]
            username1 = ""
            username2 = "None"
            Phone_number = ""
            Rescue_Center_Name = ""
            Distance = ""
            if type == 1 :
                rescueid = "Hospital"
                (username1, Distance, Rescue_Center_Name, Phone_Number) = Rescuecenter(rescueid)
                Ressendsms()
                rescueid = "Police Station"
                (username2, Distance, Rescue_Center_Name, Phone_Number) = Rescuecenter(rescueid)
                Ressendsms()
                Clisendsms()
    
            if type == 2 :
                rescueid = "Hospital"
                (username1, Distance, Rescue_Center_Name, Phone_Number) = Rescuecenter(rescueid)
                Ressendsms()
                Clisendsms()
                
            elif type == 3 :
                rescueid = "Police Station"
                (username1, Distance, Rescue_Center_Name, Phone_Number) = Rescuecenter(rescueid)
                Ressendsms()
                Clisendsms()
                
            elif type == 4 :
                rescueid = "Govt Office"
                (username1, Distance, Rescue_Center_Name, Phone_Number) = Rescuecenter(rescueid)
                Ressendsms()
                Clisendsms()
                
            elif type == 5 :
                rescueid = "Vehicle Workshop"
                (username1, Distance, Rescue_Center_Name, Phone_Number) = Rescuecenter(rescueid)
                Ressendsms()
                Clisendsms()
            
            Mod_Time = date_time
            Mod_URL = mod_image[0:6] + str("|") + mod_image[7:14]
            
            data = {
                'Rescue Center ID 1' : username1,
                'Rescue Center ID 2' : username2, 
                'Vehicle Number': Vehicle_No,
                'Date and Time': Mod_Time,
                'Phone Number': Vehicle_Phone,
                'Type': type,
                'Location':{
                'Latitude':source_lat,
                'Longitude':source_lon},
                'Image':Mod_URL
                 }
            
            db.child("Emergency History").child(Vehicle_No).set(data)
            db.child("Vehicle_Details").child(vehid).remove()
            
        else :
            time.sleep(2)


    
    


