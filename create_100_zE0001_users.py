"""

This program creates 100 test zE0001_User objects by batch POSTing them to Parse.

It first queries "_User" for users registered for this particular event,
then creates an object in the event-specific zE0001_User table for each user.


"""

# import stuff
import math
import os
import random
import sqlite3
import time
import json, httplib, urllib # parse stuff
from pprint import pprint # pretty printing


# get (query) all eligible Users
connection = httplib.HTTPSConnection('api.parse.com', 443)
params = urllib.urlencode({"where":json.dumps({
       "array_eventsRegistered": 1
     })})
connection.connect()
connection.request('GET', '/1/users?%s' % params, '', {
       "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
       "X-Parse-REST-API-Key": "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS"
     })
query_result = json.loads(connection.getresponse().read())
pprint (query_result)
num_users_registered_for_event = len(query_result['results'])
print "\nUsers Registered: " + str(num_users_registered_for_event)



# Make the zE0001_User objects (put them in a JSON object)
# and upload them to Parse (batch creation limit is 50).

# If query_result['results'] > 50, it has to be split into multiple chunks.
# Even if not, the chunk(s) will be put into an interable "for" statement.
# http://stackoverflow.com/questions/22878743/how-to-split-dictionary-into-multiple-dictionaries-fast
if num_users_registered_for_event > 50:
    chunk1 = query_result['results'][:50]
    chunk2 = query_result['results'][50:] # this should be 50 at most; I can always change it if an event has > 100 people.
    chunk_list = [chunk1, chunk2]
else:
    chunk_list = [query_result['results']]
print "\n\nLength of chunk list: " + str(len(chunk_list)) + "\n\n"


playerCounter = 1


for chunk in chunk_list: # this is done either 1x or 2x, assuming <= 100 people.

    requests_array = []

    for returned_user_object_dict in chunk: 

        new_user_object_dict = {
                        "method": "POST",
                        "path": "/1/classes/zE0001_User",
                        "body": 
                        {
                          "user_objectId": returned_user_object_dict["objectId"],
                          "playerNum": playerCounter,
                          "username": returned_user_object_dict["username"],
                          "sex": returned_user_object_dict["sex"]
                        }
        }

        requests_array.append(new_user_object_dict)

        #query_result['results'].remove(returned_user_object_dict)

        playerCounter += 1


    requests_dict_to_upload = json.dumps( { "requests": requests_array } )

    # upload them
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/batch', requests_dict_to_upload, {
           "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
           "X-Parse-REST-API-Key": "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS",
           "Content-Type": "application/json"
         })
    creation_result = json.loads(connection.getresponse().read())
    pprint (creation_result)


# # Females
# requests_dict = { "requests": [] }

# for name in fullNames_female:
#     object_dict = {
#                     "method": "POST",
#                     "path": "/1/classes/_User",
#                     "body": 
#                     {
#                       #"playerNum": playerCounter,
#                       "username": name,
#                       "array_eventsRegistered": [2],
#                       "sex": 'F'
#                     }
#     }

#     requests_dict['requests'].append(object_dict)

#     playerCounter += 1


# requests_dict_to_upload = json.dumps(requests_dict)

# # upload them
# connection = httplib.HTTPSConnection('api.parse.com', 443)
# connection.connect()
# connection.request('POST', '/1/batch', requests_dict_to_upload, {
#        "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
#        "X-Parse-REST-API-Key": "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS",
#        "Content-Type": "application/json"
#      })
# result = json.loads(connection.getresponse().read())
# pprint (result)










""" This is copied from the Parse docs for batch object creation

import json, httplib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/batch', json.dumps({
       "requests": [
         {
           "method": "POST",
           "path": "/1/classes/_User",
           "body": 
           {
             "username"  : "alexchick",
             "password"  : "1234",
             "firstName" : "Alex",
             "lastName"  : "Chick", 
           }
         },
         {
           "method": "POST",
           "path": "/1/classes/Event",
           "body": {
             "eventNumber" : 0002,
             "location"	   : "San Francisco",
             "start"	   : ["2016.10.24","20:00"]
           }
         }
       ]
     }), {
       "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
       "X-Parse-REST-API-Key": "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS",
       "Content-Type": "application/json"
     })
result = json.loads(connection.getresponse().read())
print result

"""











