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
    if value is None:
        value = []
    return '%s-%d' %(uid, len(value))

def genuid(db1,user):
    '''genuid returns a uid as a string equal to the number of registered users'''
    usercount = db1.child("UserCount").get(user['idToken']).val()
    db1.child("UserCount").set(usercount+1,user['idToken'])
    return str(usercount)

def newuser(db1, user, uid, method, token):
    ''''newuser creates a new user instance in the db'''
    data = {"method":method, "token":token, "playlists":[]}
    db1.child("UserTable").child(uid).set(data, user['idToken'])

def newplaylist(db1, user, uid, pid, name, spid, token):
    '''newplaylist implements the database side of creating a playlist
       Adds the playlist to the host user as well as creates the playlist
       in the playlist table'''
    #Add the playlist to the playlist table
    data = {"Name": name,
            "SPID": spid,
            "Owner":uid,
            "Active":True,
            "Songs":[],
            "Blacklist":[],
            "History":[],
            "Auth": token}
    db1.child("Playlists").child(pid).set(data, user['idToken'])
    #Add the playlists to the users list
    adduser(db1,user,uid,pid)

def haspermissions(db1, user, uid, pid):
    ''' haspermissions takes the uid and returns true if the user has
        permissions to write to a given playlist'''
    playlists = db1.child("UserTable").child(uid).child("playlists").get(user['idToken']).val()
    if playlists is None:
        playlists = []
    blacklist = db1.child("Playlists").child(pid).child("Blacklist").get(user['idToken']).val()
    if blacklist is None:
        blacklist = []
    return pid in playlists and uid not in blacklist

def adduser(db1, user, uid, pid):
    '''adduser adds a user to the list of users with permission to edit a playlist'''
    #Make sure this user isn't blacklisted
    blacklist = db1.child("Playlists").child(pid).child("Blacklist").get(user['idToken']).val()
    if (not blacklist is None) and (uid in blacklist):
        return
    playlists = db1.child("UserTable").child(uid).child("playlists").get(user['idToken']).val()
    if playlists is None:
        playlists = []
    playlists.append(pid)
    db1.child("UserTable").child(uid).child("playlists").set(playlists, user['idToken'])

def addsuggestedsong(db1, user, uid, pid, song):
    ''' addsuggestedsong adds a suggested song to the list of songs
        in the playlist database'''
    if not haspermissions(db1, user, uid, pid):
        return
    songs = db1.child("Playlists").child(pid).child("Songs").get(user['idToken']).val()
    #If there are no songs suggested yet
    if songs is None:
        songs = []
    songs.append(song)
    db1.child("Playlists").child(pid).child("Songs").set(songs, user['idToken'])

def testdatabase():
    '''testDB tests posting to the firebase database'''
    #Authenticating
    fb1 = firebase()
    user = signin(fb1)
    
    #Adding the users
    uid = genuid(fb1.database(),user)
    uid2 = genuid(fb1.database(),user)
    assert uid != uid2
    
    #Add first user
    newuser(fb1.database(), user, uid, "GOOGLE", "1234567")
    fb1.database().child("UserTable").child(uid).update({"playlists": [genplaylistid(fb1.database(),user,uid)]}, user["idToken"])
    assert not fb1.database().child("UserTable").child(uid) is None
    
    #Add a new playlist
    pid = genplaylistid(fb1.database(), user, uid)
    assert pid == ("%s-1" % uid)
    newplaylist(fb1.database(), user, uid, pid, "TestPlaylist", "12345", "678910")
    assert not fb1.database().child("Playlists").child(pid) is None
    assert haspermissions(fb1.database(), user, uid, pid)
    
    #add a song to the playlist
    addsuggestedsong(fb1.database(), user, uid, pid, "testsong")
    addsuggestedsong(fb1.database(), user, uid, pid, "test2")
    assert "testsong" in fb1.database().child("Playlists").child(pid).child("Songs").get(user['idToken']).val()
    assert "test2" in fb1.database().child("Playlists").child(pid).child("Songs").get(user['idToken']).val()
    
    #Add a user to the playlist
    newuser(fb1.database(), user, uid2, "FACEBOOK", "2345678")
    assert not haspermissions(fb1.database(), user, uid2, pid)
    adduser(fb1.database(), user, uid2, pid)
    assert haspermissions(fb1.database(), user, uid2, pid)

    #Cleanup
    db1 = fb1.database()
    db1.child("UserTable").child(uid).remove(user['idToken'])
    db1.child("UserTable").child(uid2).remove(user['idToken'])
    db1.child("Playlists").child(pid).remove(user['idToken'])
    usercount = db1.child("UserCount").get(user['idToken']).val()
    db1.child("UserCount").set(usercount-2, user['idToken'])

if __name__ == '__main__':
    testdatabase()
