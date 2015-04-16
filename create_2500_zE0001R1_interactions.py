#############################
#                           #
#     Alexander Chick       #
#                           #
#          ©2015            #
#                           #
#############################

"""

This program creates 50 * 50 = 2500 test interaction objects in the "zE0001R1" table in Parse.

Data members for each Round 1 interaction object:

- interaction (int from 1 to 2500)
- subround (int from 1 to 50)
- station (int from 1 to 50)
- iPad_objectId (a string? pointer?)
- m_objectId (a string? pointer?)
- f_objectId (a string? pointer?)
- m_playerNum (int)
- f_playerNum (int)
- m_firstName (string)
- f_firstName (string)
- question_objectId (a string? pointer?)
- m_answer (string? or int of array position 0-3? or array of [int, string]?)
- f_answer (string? or int of array position 0-3?)
- is_same_answer (boolean)
- m_see_f_again (string or int 1-4?)
- f_see_m_again (string or int 1-4?)
- total_see_again (int, sum of see again ints, so possible values are 2-8)
- m_next_station (int)
- f_next_station (int, current + 1)

I'm going to start by just using strings
to reference objectId's, 
and I'll figure out later if it'll be
better or more helpful to use pointers.

I'm also going to try to use ParsePy, 
which I *think* is meant to make it easier
to interact with Parse in Python.

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





# calling "register" allows parse_rest / ParsePy to work
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")



#
# 1. Get (query) all "zE0001_User" objects (the people at the event)
#
connection = httplib.HTTPSConnection('api.parse.com', 443)
params = urllib.urlencode({"order":"-sex,playerNum"}) # retrieves males first then females, in ascending order by playerNum
connection.connect()
connection.request('GET', '/1/classes/zE0001_User?%s' % params, '', {
       "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
       "X-Parse-Master-Key": "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
     }) 
query_result = json.loads(connection.getresponse().read())
#pprint (query_result)
num_people_at_event = len(query_result['results'])
print num_people_at_event

#
#
#






















































