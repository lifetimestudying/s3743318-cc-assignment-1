from google.cloud import datastore

datastore_client = datastore.Client()

# add user into datastore
def storeUser(userID, username, password):
    entity = datastore.Entity(key=datastore_client.key('userID',userID)) 
    entity.update({
        'username': username,
        'password': password
    })

    datastore_client.put(entity) 

# check if userID and password matches data in datastore
def validateUser(userID, password):
    key = datastore_client.key("userID", userID)
    user = datastore_client.get(key)

    if not user is None:
        if user["password"] == password:
            return True

        
    return False

# check if userID already been registered 
def checkUser(userID):
    key = datastore_client.key("userID", userID)
    user = datastore_client.get(key)

    if user is None:
        return True
    
    return False



