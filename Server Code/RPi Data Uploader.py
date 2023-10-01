import pyrebase

config = {
  "apiKey": "################",
  "authDomain": "minor-proj.firebaseapp.com",
  "databaseURL": "https://minor-proj.firebaseio.com",
  "storageBucket": "minor-proj"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()


Phone_no=#########
Vehicle_no="KA11-F-9999"
lat_degrees="12.528376"
long_degrees="76.893456"
image="https://www.dropbox.com/s/r4ag9zi0ud8ie5t/picture.jpg?dl=0\n"
type=4
data = {
        'Image':image,
        'Location':{
        'Latitude':lat_degrees,
        'Longitude':long_degrees},
        'Phone Number': Phone_no ,
        'Vehicle Number': Vehicle_no,
        'Type': type }
db.child("Vehicle_Details").push(data)
print("Creating Done")
