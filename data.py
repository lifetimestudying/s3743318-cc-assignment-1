from google.cloud import datastore, storage

# datastore client
datastore_client = datastore.Client()

# storage client
storage_client = storage.Client()
# identify bucket from storage client
bucket = storage_client.get_bucket('s3743318-assignmnet-1.appspot.com')

# add user into datastore
def storeUser(userID, username, password, imageFileName, imageFile):
    entity = datastore.Entity(key=datastore_client.key('userID',userID)) 
    entity.update({
        'username': username,
        'password': password
    })

    datastore_client.put(entity) 
    uploadImage(imageFileName, imageFile)

# check if userID and password matches data in datastore
def validateUser(userID, password):
    key = datastore_client.key("userID", userID)
    user = datastore_client.get(key)

    if not user is None:
        if user["password"] == password:
            return True
        
    return False

# check if userID already been registered 
def checkUserID(userID):
    id_key = datastore_client.key("userID", userID)
    user_id = datastore_client.get(id_key)

    # return true if userID not exists in datastore
    if user_id is None:
        return True

    return False


# check if username already been registered
def checkUsername(username):
    query = datastore_client.query(kind="userID")
    query.add_filter("username", "=", username)
    results = list(query.fetch())

    if len(results) == 0:
        return True
    
    return False

# upload image into storage
def uploadImage(imageFileName, imageFile):
    blob = bucket.blob(imageFileName)
    blob.upload_from_file(imageFile)

