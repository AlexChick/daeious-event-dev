#############################
#                           #
#     Alexander Chick       #
#                           #
#     copyright  2015       #
#                           #
#############################

"""

This program creates 50 * 50 = 2500 test interaction objects 
	in the "zE0001R1" table in Parse.

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
- is_same_answer (boolean) (will be filled in by play_zE0001R1.py)
- m_see_f_again (string or int 1-4?)
- f_see_m_again (string or int 1-4?)
- total_see_again (int, sum of see again ints, so possible values are 2-8)
- m_next_station (int)
- f_next_station (int, current + 1)
- ACL (will work on this later)

I'm going to start by just using strings
	to reference objectId's, 
	and I'll figure out later if it'll be
	better or more helpful to use pointers.

I'm also going to try to use ParsePy, 
	which I *think* is meant to make it easier
	to interact with Parse in Python.

Eventually, I can put the code in these files into functions,
	and have a simulate_zE0001 function to simulate a game 
	being setup, played, an analyzed.

The ParsePy docs are at 
	https://github.com/dgrtwo/ParsePy.

**************************************************

Here's the order of everything:

1. Get (query) all "zE0001_User" objects (the people at the event)
		- all_users_at_event is an array containing the objects

2. Get (query) the correct iPads / "IPad" objects for the event (right now, get all 100)
		- all_ipads_at_event is an array containing the objects

3. Get (query) the correct questions / "Question" objects for the event (right now, get all 100)
		- all_questions_at_event is an array containing the objects

4. Create the interaction / zE####R1 objects, store them in an array,
   create a ParseBatcher, and upload the objects by calling batch_save
   on the batcher, passing the array as an argument. 
   		- The Parse batch upload limit is 50, so this has to be 
   		  in some kind of loop.
   		- Use counters, formatted like: interaction_counter, subround_counter 




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
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
		 "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
		 master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
	)


##################################################



""" _______________________________________________

	1. Get (query) all "zE0001_User" objects (the people at the event)

		- all_users_at_event is an array containing the objects
		- create all_males_at_event, all_females_at_event too	
		- use ParsePy / parse_rest
 		- (should I use the Parse "count" function?)
 		- Queries return arrays of objects.
 		- an object's attributes are accessed like this: 
	              object.attribute
	      For example, to get the username of playerNum = 1:
	              all_users_at_event[0].username
    _______________________________________________
    ----------------------------------------------- """

# set the class name of the event users we're querying
eventUserClassName = "zE0001_User"
	# (The precise 4-digit number can be retrieved / set by querying "Config"; 
	# I'll add this functionality later. Maybe I can pass an argument 
	# containing the event number into the function that runs the simulation.)

# make it a subclass of Object
eventUserClass = Object.factory(eventUserClassName)

# run the query (all users at event)
all_users_at_event = eventUserClass.Query.all().order_by("playerNum")
	# This has a format of [object, object, object, ...]
	# and an object's attributes are accessed like this: 
	#   object.attribute
	# For example, to get the username of playerNum = 1:
	#   all_users_at_event[0].username

# run the query (all males at event)
all_males_at_event = eventUserClass.Query.all().filter(sex='M').order_by("playerNum")

# run the query (all females at event)
all_females_at_event = eventUserClass.Query.all().filter(sex='F').order_by("playerNum")

# print the results of the queries
print "\n\n" + str(len(all_users_at_event)) + " people are at this event.\n"
print "\n\n" + str(len(all_males_at_event)) + " males are here.\n"
print "\n\n" + str(len(all_females_at_event)) + " females are here.\n"



""" _______________________________________________

	2. Get (query) the correct iPads / "IPad" objects for the event (right now, get all 100)
		
		- all_ipads_at_event is an array containing the objects
    _______________________________________________
    ----------------------------------------------- """

# make IPad a subclass of Object
class IPad(Object):
	pass

# run the query
all_ipads_at_event = IPad.Query.all().order_by("iPad_Id")




""" _______________________________________________

	3. Get (query) the correct questions / "Question" objects for the event (right now, get all 100)
		
	    - all_questions_at_event is an array containing the objects
    _______________________________________________
    ----------------------------------------------- """

# make Question a subclass of Object
class Question(Object):
	pass

# run the query
all_questions_at_event = Question.Query.all().order_by("questionNum")




""" _______________________________________________

    4. Create the interaction / zE####R1 objects, store them in an array,
    create a ParseBatcher, and upload the objects by calling batch_save
    on the batcher, passing the array as an argument. 
   		- The Parse batch upload limit is 50, so this has to be 
   		  in some kind of loop.
   		- Use counters, formatted like: interaction_counter, subround_counter 
    _______________________________________________
    ----------------------------------------------- """

# set the class name of the round for which we're creating interactions
eventRoundClassName = "zE0001R1"
	# (The precise 4-digit number can be retrieved / set by querying "Config"; 
	# I'll add this functionality later. Maybe I can pass an argument 
	# containing the event number into the function that runs the simulation.)

# make it a subclass of Object
eventRoundClass = Object.factory(eventRoundClassName)

# # set the class's ACL - doesn't work right now
# zE0001R1.ACL.set_default(read = False, write = False)

# initiate counters
interaction_counter = 0

# initialize the list of stations [1, 2, 3, ..., 50]
station_list = list(x+1 for x in range(50))

# iterate through the males, 
for event_user_object in all_males_at_event:

	# initialize the list of objects to pass to the batch uploader
	interactions_list_to_be_saved = []

	# iterate through subrounds
	for i in range (50):

		interaction_counter += 1

		interaction = eventRoundClass(

			interaction = interaction_counter,
			subround = (i + 1),
			station = station_list[i],
			iPad_objectId = all_ipads_at_event[i].objectId,
			m_thisEvent_objectId = all_males_at_event[0].objectId,
			f_objectId = all_females_at_event[i].objectId,
			m_user_objectId = all_males_at_event[0].user_objectId,
			f_user_objectId = all_females_at_event[i].user_objectId,			
			m_playerNum = all_males_at_event[0].playerNum,
			f_playerNum = all_females_at_event[i].playerNum,
			m_firstName = all_males_at_event[0].username,
			f_firstName = all_females_at_event[i].username,
			question_objectId = all_questions_at_event[0].objectId,
			# m_answer = None,
			# f_answer = None,
			# is_same_answer = None,
			# m_see_f_again = None,
			# f_see_m_again = None,
			# total_see_again = None,
			m_next_station = ( (station_list[i] + 1) % 50 ),
			f_next_station = ( (station_list[i] - 1) if station_list[i] > 1 else 50 )# need to fix 50 --> 0 instead of 50 --> 1

		)

		# add to interactions_list_to_be_saved
		interactions_list_to_be_saved.append(interaction)

	# save these 50 interactions to Parse
	batcher = ParseBatcher()
	batcher.batch_save(interactions_list_to_be_saved)
	print "batch " + str(event_user_object.playerNum) + " saved."

	# wait approx. 1-2 seconds so as not to exceed Parse's 30 requests / second free limit.
			# Without waiting, I get this error: 
			# parse_rest.core.ResourceRequestBadRequest: {"code":155,"error":"This application performed 1805 requests within the past minute, and exceeded its request limit. Please retry in one  minute or raise your request limit."}
	time.sleep(2)



	# rotate lists


print "All batches saved."


















# # 1. Get (query) all "zE0001_User" objects (the people at the event)
# #		- by directly calling the Parse API through HTTP

# connection = httplib.HTTPSConnection('api.parse.com', 443)
# params = urllib.urlencode({"order":"-sex,playerNum"}) # retrieves males first then females, in ascending order by playerNum
# connection.connect()
# connection.request('GET', '/1/classes/zE0001_User?%s' % params, '', {
#        "X-Parse-Application-Id": "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ",
#        "X-Parse-Master-Key": "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
#      }) 
# query_result = json.loads(connection.getresponse().read())
# #pprint (query_result)
# num_people_at_event = len(query_result['results'])
# print num_people_at_event












































