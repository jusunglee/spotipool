"""database contains the interface to interact with the firebase backend"""
import pyrebase


def firebase():
    """fireBase returns a firebase instance to be used when posting/reading from the database"""
    config = {
        "apiKey": "AIzaSyCG5371lAsnsLMTtcSV5IirInICeuLOZDM",
        "authDomain": "spotipool-ff2b7.firebaseapp.com",
        "databaseURL": "https://spotipool-ff2b7.firebaseio.com",
        "storageBucket": "spotipool-ff2b7.appspot.com"
    }

    return pyrebase.initialize_app(config)

def push(db1, user, key, val):
    """push takes a datbase reference a key and val as strings and pushes them
     to the given database. No return value"""
    db1.child(key).set(val, user['idToken'])

def testdatabase():
    '''testDB tests posting to the firebase database'''
    fb1 = firebase()
    auth = fb1.auth()
    user = auth.sign_in_with_email_and_password("test@spotipool.com", "spotipool")
    push(firebase().database(), user, "test", "value")

testdatabase()
