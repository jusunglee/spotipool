"""database contains the interface to interact directly with the firebase backend"""
import pyrebase


def firebase():
    """fireBase returns a firebase instance to be used when posting/reading from the database"""
    keys = "keys/api_auth.txt"
    with open(keys) as file_:
        content = file_.readlines()

    config = dict()

    for line in content:
        tokens = line.split('=')
        tokens = [token.strip() for token in tokens]
        config[tokens[0]] = tokens[1]

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

def genplaylistid(db1, user, uid):
    '''genplaylistid returns a playlist id consisting of uid-x
    where x is the number of playlists assigned to the uid'''
    playlists = db1.child("UserTable").child(uid).child("playlists").get(user['idToken'])
    value = playlists.val()
    stringlist = value.split(",")
    return '%s-%d' %(uid, len(stringlist))

def newuser(db1, user, uid, method, token):
    ''''newuser creates a new user instance in the db'''
    data = {"method":method, "token":token, "playlists":"[]"}
    db1.child("UserTable").child(uid).set(data, user['idToken'])

def newplaylist(db1, user, uid, pid, name, spid, token):
    #Add the playlist to the playlist table
    data = {"Name": name,
            "SPID": spid,
            "Owner":uid,
            "Active":True,
            "Songs":"",
            "Blacklist":"",
            "History":"",
            "Auth": token}
    db1.child("Playlists").child(pid).set(data, user['idToken'])
    #Add the playlists to the users list
    playlists = db1.child("UserTable").child(uid).child("playlists").get(user['idToken'])
    playlists = playlists.val()
    playlists = playlists.strip("[]").split(",")
    playlists.append(pid)
    db1.child("UserTable").child(uid).child("playlists").set(playlists,user['idToken'])


def testdatabase():
    '''testDB tests posting to the firebase database'''
    fb1 = firebase()
    user = signin(fb1)
    newuser(fb1.database(), user, "test", "GOOGLE", "1234567")
    #data = {"Method": "Google","Token":"1234567","playlists":"[1243-7,2345-6,35678-10]"}
    fb1.database().child("UserTable").child("test").update({"playlists": "[1243-7,2345-6,35678-10]"}, user["idToken"])
    pid = genplaylistid(fb1.database(),user,"test")
    newplaylist(fb1.database(),user,"test",pid,"TestPlaylist","12345","678910")

testdatabase()
