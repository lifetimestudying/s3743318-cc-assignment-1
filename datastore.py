from google.cloud import datastore

datastore_client = datastore.Client()

def storeUser(userID, username, password):
    entity = datastore.Entity(key=datastore_client.key('userID',userID)) 
    entity.update({
        'username': username,
        'password': password
    })

    datastore_client.put(entity) 

def validateUser(userID, password):
    key = datastore_client.key("userID", userID)
    user = datastore_client.get(key)

    if not user is None:
        if user["password"] == password:
            return True

        
    return False







