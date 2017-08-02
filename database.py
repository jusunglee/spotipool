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

def signin(fb1):
    '''signin returns the user token for the given firebase instance'''
    #load in the firebase authentication info from a file
    keys = "keys/db_auth.txt"
    with open(keys) as file_:
        content = file_.readlines()

    authinfo = dict()

    for line in content:
        tokens = line.split('=')
        tokens = [token.strip() for token in tokens]
        authinfo[tokens[0]] = tokens[1]

    auth = fb1.auth()
    return auth.sign_in_with_email_and_password(authinfo["email"], authinfo["password"])

def testdatabase():
    '''testDB tests posting to the firebase database'''
    user = signin(firebase())
    push(firebase().database(), user, "test", "value")

testdatabase()
