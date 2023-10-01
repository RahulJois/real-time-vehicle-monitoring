import pyrebase
import time

ttime = time.strftime('%H%M%S')

config = {
  "apiKey": "##################",
  "authDomain": "minor-proj.firebaseapp.com",
  "databaseURL": "https://minor-proj.firebaseio.com",
  "storageBucket": "minor-proj"
}


firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.child("Vehicle_Details").child("Dummy Node").set({
    'Data':'None'
    }
    )
print("Done")
