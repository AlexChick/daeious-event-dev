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
		
		- create all_males_at_event, all_females_at_event too	
		
		- use ParsePy / parse_rest
 		
 		- (should I use the Parse "count" function?)
 		
 		- a Query returns a "QuerySet" of objects. 
 		
 		- QuerySets are like lists, but you can't operate on them:
 		(AttributeError: 'Queryset' object has no attribute 'insert'),
 		so I cast each QuerySet as a list.
 		
 		- an object's attributes are accessed like this: > object.attribute
	      For example, to get the username of playerNum = 1: > all_users_at_event[0].username


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


**************************************************

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

# start program timer
program_start_time = time.time()

# Calling "register" allows parse_rest / ParsePy to work.
# - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
		 "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
		 master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
	)

# get correct event object from Parse; 
# have to subclass Object before using Event.Query
class Event(Object):
	pass
event_object = list(Event.Query.get(eventNumber = 1))
# (do I need to make this a list?)


##################################################



""" _______________________________________________

	1. Get (query) all "zE0001_User" objects (the people at the event)

		- all_users_at_event is an array containing the objects
		
		- create all_males_at_event, all_females_at_event too	
		
		- use ParsePy / parse_rest
 		
 		- (should I use the Parse "count" function?)
 		
 		- a Query returns a "QuerySet" of objects. 
 		
 		- QuerySets are like lists, but you can't operate on them:
 		(AttributeError: 'Queryset' object has no attribute 'insert'),
 		so I cast each QuerySet as a list.
 		
 		- an object's attributes are accessed like this: > object.attribute
	      For example, to get the username of playerNum = 1: > all_users_at_event[0].username
    _______________________________________________
    ----------------------------------------------- """


def get_eventUserClassName(event_number):

	# Should I use a switch block instead? Can I with ranges?

	# set the class name of the event users we're querying
	num_string = ""
	if 0 < event_number < 10:
		num_string = "000{}".format(event_number)
	elif 10 <= event_number < 100:
		num_string = "00{}".format(event_number)
	elif 100 <= event_number < 1000:
		num_string = "0{}".format(event_number)
	elif 1000 <= event_number < 10000:
		num_string = "{}".format(event_number)
	else:
		raise ValueError("The event number must be between 1 and 9999.")

	return "zE{}_User".format(num_string)




# set the class name of the event users we're querying
#eventUserClassName = "zE0001_User"
eventUserClassName = get_eventUserClassName(event_object.eventNumber)
	# (The event number can be retrieved / set by querying "Config"; 
	# I'll add this functionality later.) 

# make it a subclass of Object
eventUserClass = Object.factory(eventUserClassName)

# Queries return with a format of [object, object, object, ...]
# and an object's attributes are accessed like this: 
#   object.attribute
# For example, to get the username of playerNum = 1:
#   all_users_at_event[0].username

# run the query (all users at event)
all_users_at_event = list(eventUserClass.Query.all().order_by("playerNum"))

# run the query (all males at event)
all_males_at_event = list(eventUserClass.Query.all().filter(sex='M').order_by("playerNum"))

# run the query (all females at event)
all_females_at_event = list(eventUserClass.Query.all().filter(sex='F').order_by("playerNum"))

# run the query (all ghosts at event)
all_ghosts_at_event = list(eventUserClass.Query.all().filter(sex='G').order_by("playerNum"))

# print the results of the queries
print "\n\n{} of the {} people who registered for this event are here.\n".format(len(all_users_at_event), event_object.numPeople)
print "\n\n{} of the {} men are here.\n".format(len(all_males_at_event), event_object.numMen)
print "\n\n{} of the {} women are here.\n".format(len(all_females_at_event), event_object.numWomen)
print "\n\n{} \"ghosts\" are being provided.\n".format(len(all_ghosts_at_event))
print "\n\n{} iPads and {} iPad stations are required for this event.".format(event_object.numIPads, event_object.numStations)



""" _______________________________________________

	2. Get (query) the correct iPads / "IPad" objects for the event (right now, get all 100)
		
		- all_ipads_at_event is an array containing the objects
    _______________________________________________
    ----------------------------------------------- """

# make IPad a subclass of Object
class IPad(Object):
	pass

# run the query
all_ipads_at_event = list(IPad.Query.all().order_by("iPad_Id"))




""" _______________________________________________

	3. Get (query) the correct questions / "Question" objects for the event (right now, get all 100)
		
	    - all_questions_at_event is an array containing the objects
    _______________________________________________
    ----------------------------------------------- """

# make Question a subclass of Object
class Question(Object):
	pass

# run the query
all_questions_at_event = list(Question.Query.all().order_by("questionNum"))




""" _______________________________________________

    4. Create the interaction / zE####R1 objects, store them in an array,
    create a ParseBatcher, and upload the objects by calling batch_save
    on the batcher, passing the array as an argument. 
   		- The Parse batch upload limit is 50, so this has to be 
   		  in some kind of loop.
   		- Use counters.
    _______________________________________________
    ----------------------------------------------- """

# set the class name of the round for which we're creating interactions (zE####R1)
eventRoundClassName = eventUserClassName[:6] + "R1"

# make it a subclass of Object
eventRoundClass = Object.factory(eventRoundClassName)

# # set the class's ACL - doesn't work right now
# zE0001R1.ACL.set_default(read = False, write = False)

# initiate counters
interaction_counter = 0

# initialize the list of stations [1, 2, 3, ..., 50]
station_list = list(x+1 for x in range(50))

batch_uploading_start_time = time.time()

# iterate through the subrounds -- i.e. subround 1 contains interactions 1-50, etc.
for subround in range (50):

	# initialize the list of created objects to pass to the batch uploader
	interactions_list_to_be_saved = []

	# create the 50 interactions of this subround
	for i in range (50):

		interaction_counter += 1

		interaction = eventRoundClass(

			interaction = 	interaction_counter,
			subround = 		subround + 1,
			station = 		station_list[i],

			inner_iPad_objectId = all_ipads_at_event[i].objectId,
			outer_iPad_objectId = all_ipads_at_event[i+50].objectId,

			m_thisEvent_objectId = 	all_males_at_event[i].objectId,
			f_thisEvent_objectId = 	all_females_at_event[i].objectId,

			m_user_objectId = 	all_males_at_event[i].user_objectId,
			f_user_objectId = 	all_females_at_event[i].user_objectId,

			m_playerNum = 	all_males_at_event[i].playerNum,
			f_playerNum = 	all_females_at_event[i].playerNum,

			m_firstName = 	all_males_at_event[i].username,
			f_firstName = 	all_females_at_event[i].username,

			question_objectId = 	all_questions_at_event[i].objectId,
			# m_answer = None,
			# f_answer = None,
			# is_same_answer = None,

			# m_see_f_again = None,
			# f_see_m_again = None,
			# total_see_again = None,

			m_next_station = ( (station_list[i] + 1) % 50 if station_list[i] !=  ),
			f_next_station = ( (station_list[i] - 1) if station_list[i] > 1 else 50 )

		)

		# add to interactions_list_to_be_saved
		interactions_list_to_be_saved.append(interaction)


	# wait approx. 1-2 seconds so as not to exceed Parse's 30 requests / second free limit.
		# Without waiting, I get this error: 
		# parse_rest.core.ResourceRequestBadRequest: {"code":155,"error":"This application performed 1805 requests within the past minute, and exceeded its request limit. Please retry in one  minute or raise your request limit."}
		# Times that work: 2.0
		# Times that don't work: 0.5 (does 35 of 50), 1.0 (does 47 of 50)
	#time.sleep(1)

	# if we're going too fast for the request limit of 1800 per minute, slow down
	# Test 1: Slept after batch 35 for 47.557 seconds. Success (no errors, all batches saved).
	# Test 2: Slept after batch 35 for 49.203 seconds. Success.
	# Test 3: Slept after batch 35 for 45.496 seconds. Success.

	time_uploading_before_sleep = time.time() - batch_uploading_start_time
	if (time_uploading_before_sleep < 60) and (interaction_counter > 1799):
		print "\nSleeping for {} seconds.".format(round((60 - time_uploading_before_sleep), 3))
		pause_time = time.time()
		time.sleep(60 - time_uploading_before_sleep)
		print "\nUploading will now resume.\n"
		resume_time = time.time()

	# save these 50 interactions to Parse
	batcher = ParseBatcher()
	batcher.batch_save(interactions_list_to_be_saved)
	print "batch " + str(subround + 1) + " of 50 has been saved."



	# rotate lists
	# (I'm getting an error that says "Slice is not supported for now.",
	# so I've had to do something slightly more complicated.)

	# males: take the last, put in front 
	# (guys are moving toward increasing station nums)
	all_males_at_event.insert(0, all_males_at_event[-1])
	all_males_at_event.pop(-1) # default is -1, but I left it in for clarity

	# females: take the first, put in back 
	# (girls are moving toward decreasing station nums)
	all_females_at_event.append(all_females_at_event[0])
	all_females_at_event.pop(0)
	
	# iPads: will iterate as stations do 
	# (an iPad always stays at the same station)
	
	# questions: take the first two, put in back
	all_questions_at_event.append(all_questions_at_event[0])
	all_questions_at_event.append(all_questions_at_event[1])
	all_questions_at_event.pop(0)
	all_questions_at_event.pop(0)

	# rotate lists (with slicing)
	# (ParsePy doesn't support slicing lists of objects yet)
	# # males: take the first, put in back
	# all_males_at_event = all_males_at_event[1:] + [all_males_at_event[0]]
	# # females: take the last, put in front
	# all_females_at_event = [all_females_at_event[-1]] + all_females_at_event[:-1]
	# # questions: take the first two, put in back
	# all_questions_at_event = all_questions_at_event[2:] + all_questions_at_event[:2]

program_end_time = time.time()

print "\nAll batches saved."


# Timing tests

print "\nTime spent uploading: {} seconds.".format(round((pause_time - program_start_time) + (program_end_time - resume_time), 3))
print "\nTime spent sleeping: {} seconds.".format(round((resume_time - pause_time), 3))
print "\nTotal time of program: {} seconds.\n".format(round((program_end_time - program_start_time), 3))

"""
TESTS

******

From laptop, at home:

Time spent uploading: 19.552 seconds.
Time spent sleeping: 48.067 seconds.
Total time of program: 67.618 seconds.

Time spent uploading: 18.309 seconds.
Time spent sleeping: 47.767 seconds.
Total time of program: 66.076 seconds.

Time spent uploading: 19.194 seconds.
Time spent sleeping: 47.814 seconds.
Total time of program: 67.008 seconds.

******

From laptop, at Dana Farber:

Time spent uploading: 32.592 seconds.
Time spent sleeping: 38.232 seconds.
Total time of program: 70.824 seconds.


"""










































