import pandas as pd
from firebase_admin import credentials, db
import firebase_admin

def GetDataFromFirebase(JSON_DB_File:str="db-cred.json",
                        ProjectID:str = "handwash-detection-db-001",
                        databaseURL:str = "handwash-detection-db-001.firebaseapp.com"):
    cred = credentials.Certificate(JSON_DB_File)
    Config = {
      apiKey: "AIzaSyCqZaOX3s6zIeCwv_r73_7EX_aBCDzAxno",
      authDomain: "handwash-detection-db-001.firebaseapp.com",
      databaseURL: "https://handwash-detection-db-001-default-rtdb.firebaseio.com",
      projectId: "handwash-detection-db-001",
      storageBucket: "handwash-detection-db-001.appspot.com",
      messagingSenderId: "857179695665",
      appId: "1:857179695665:web:1435b9041fc8df3555c310",
      measurementId: "G-R2S4KD4YNV"
    }

    firebase_admin.initialize_app(cred, Config)
    ref = db.reference("/")
    data = ref.get()
    df = pd.DataFrame(data)
    df = df.rename_axis('Time').reset_index()
    df.sort_values(by='Time', inplace=True)
    df = df.drop(columns=['LED_VAL'])
    return df

database = GetDataFromFirebase()#.fillna("No Detection happended this Time")
