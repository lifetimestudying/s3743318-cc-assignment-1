from google.cloud import datastore, storage, vision
import os
# datastore client
datastore_client = datastore.Client()

# storage client
storage_client = storage.Client()
# identify bucket from storage client
bucket = storage_client.get_bucket('s3743318-assignmnet-1.appspot.com')
# vision client
vision_client = vision.ImageAnnotatorClient()

# add user into datastore
def storeUser(userID, username, password, imageFile):
    entity = datastore.Entity(key=datastore_client.key('userID',userID)) 
    entity.update({
        'username': username,
        'password': password
    })

    datastore_client.put(entity) 
    uploadImage(userID, imageFile)

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
def uploadImage(userID, imageFile):

    # inital gcloud storage dir and upload file name
    imageFileName = "%s/%s" % ('uploads', userID + 'fileImage.jpg')
    # setup dir and object on storage bucket
    blob = bucket.blob(imageFileName)
    # upload image to bucket 
    blob.upload_from_file(imageFile)
    # make object public accessable
    blob.make_public()

# retrieve image file of user
def getImage(userID):

    # initial public access url
    auth_url = f"https://storage.googleapis.com/s3743318-assignmnet-1.appspot.com/uploads/{userID}fileImage.jpg"
    
    return auth_url 
    
#
    