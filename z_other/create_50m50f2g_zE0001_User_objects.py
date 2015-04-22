"""

This program creates 100 test zE0001_User objects by batch POSTing them to Parse.

It first queries "_User" for users registered for this particular event,
then creates an object in the event-specific zE0001_User table for each user.

Right now, the code is cluttered.

I plan to use ParsePy and the parse_rest API to make it a lot cleaner.


"""

# import stuff
import math
import os
import random
import sqlite3
import time
import json, httplib, urllib # parse stuff
from pprint import pprint # pretty printing
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")


# get (query) all eligible Users
class _User(Object):
  pass

all_users_at_event = list(_User.Query.filter(array_eventsRegistered = event_object.eventNumber))

for user in all_users_at_event:



connection = httplib.HTTPSConnection('api.parse.com', 443)
params = urllib.urlencode({"where":json.dumps({
       "array_eventsRegistered": 1
     })})
connection.connect()
connection.request('GET', '/1/users?%s' % params, '', {
       "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
       "X-Parse-Master-Key": "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
     })
query_result = json.loads(connection.getresponse().read())
pprint (query_result)
num_users_registered_for_event = len(query_result['results'])
print "\nUsers Registered: " + str(num_users_registered_for_event)




# set the class name of the event users we're creating
eventUserClassName = "zE0001_User"
  # (The precise 4-digit number can be retrieved / set by querying "Config"; 
  # I'll add this functionality later. Maybe I can pass an argument 
  # containing the event number into the function that runs the simulation.)

# make it a subclass of Object
eventUserClass = Object.factory(eventUserClassName)




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
    pprint (str(len(creation_result)) + " zE0001_User objects created in Parse.")











