from google.cloud import datastore, storage

# datastore client
datastore_client = datastore.Client()

# storage client
storage_client = storage.Client()

# identify bucket from storage client
bucket = storage_client.get_bucket('s3743318-assignmnet-1.appspot.com')

# add user into datastore
def storeUser(userID, username, password, imageFile):
    # retrieve entity by kind name
    entity = datastore.Entity(datastore_client.key('user')) 
    # key not set which will be auto generated by gcloud
    entity.update({
        'userID': userID,
        'username': username,
        'password': password
    })

    datastore_client.put(entity) 
    # upload user image to user storage
    uploadUserImage(userID, imageFile)

# add post into datastore
def storePost(userID, subject, postMessage, dt, imageFile):
    # retrieve entity by kind name
    entity = datastore.Entity(key=datastore_client.key('post'))
    # key not set which will be auto generated by gcloud
    entity.update({
        'userID': userID,
        'subject': subject,
        'postMessage': postMessage,
        'datetime': dt
    })

    datastore_client.put(entity)
    # upload post image to post storage
    uploadPostImage(userID, subject, imageFile)

# check if userID and password matches data in datastore
def validateUser(userID, password):
    query = datastore_client.query(kind="user")
    query.add_filter("userID", "=", userID)
    query.add_filter("password", "=", password)

    results = list(query.fetch())

    if len(results) != 0:
        return True

    return False

# check if userID already been registered 
def checkUserID(userID):
    query = datastore_client.query(kind="user")
    query.add_filter("userID", "=", userID)
    results = list(query.fetch())

    # return true if userID not exists in datastore
    if len(results) == 0:
        return True

    return False


# check if username already been registered
def checkUsername(username):
    query = datastore_client.query(kind="user")
    query.add_filter("username", "=", username)
    results = list(query.fetch())

    if len(results) == 0:
        return True
    
    return False


def uploadUserImage(userID, imageFile):
    # inital gcloud storage dir and upload file name
    imageFileName = "%s/%s.jpg" % ('userImage', userID)
    # setup dir and object on storage bucket
    blob = bucket.blob(imageFileName)
    # upload image to bucket 
    blob.upload_from_file(imageFile)
    # make object public accessable
    blob.make_public()


def uploadPostImage(userID, dt, imageFile):
    # inital gcloud storage dir and upload file name
    imageFileName = "%s/%s%s.jpg" % ('postImage', userID, dt)
    # setup dir and object on storage bucket
    blob = bucket.blob(imageFileName)
    # upload image to bucket 
    blob.upload_from_file(imageFile)
    # make object public accessable
    blob.make_public()


# retrieve image file of user
def getUserImage(userID):
    # initial public access url
    auth_url = f"https://storage.googleapis.com/s3743318-assignmnet-1.appspot.com/userImage/{userID}.jpg"
    return auth_url 
    

# retrieve post image
def getPostImage(userID, dt):
    auth_url = f"https://storage.googleapis.com/s3743318-assignmnet-1.appspot.com/postImage/{userID}{dt}.jpg"
    return auth_url 


def getUserPost(userID):
    query = datastore_client.query(kind="post")
    query.add_filter("userID", "=", userID)
    query.order = ["-datetime"]

    results = list(query.fetch())

    return results


def updatePassword(userID, password):
    query = datastore_client.query(kind="user")
    query.add_filter("userID", "=", userID)

    data = query.fetch()

    for value in data:
        value['password'] = password
        datastore_client.put(value)


def updatePost(userID, subject, postMessage, olddatetime, datetime, image):
    query = datastore_client.query(kind="post")
    query.add_filter("userID", "=", userID)
    query.add_filter("datetime", "=", olddatetime)

    data = query.fetch()

    for value in data:
        value['postMessage'] = postMessage
        value['subject'] = subject
        value['datetime'] = datetime

        datastore_client.put(value)
         





