"""
"""

###############################################################################

# Import Python stuff
from __future__ import print_function
from pprint import pprint
import itertools
import math
import os
import random
import sys
import time

# Import Parse stuff
import httplib, json, urllib

# Import ParsePy stuff
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

###############################################################################

def prepare_R1(m, f, mg, fg, ep, li_eu):
	"""
	(males, females, male ghosts, female ghosts)

	Create Round-1 Interactions.

	For now, station Nums, iPad Nums, etc. start at 1, 2, 3, ...,
	but that will be changed so that the correct Nums are chosen 
	and put into lists.

	(It's tricky to do these random simulations because to make it realistic
		I'd have to pull only those objects with array_eventsRegistered 
		containing the eNum. To truly randomize things, I guess I could
		create an event with a random number of men and women every time...
		and while that seems like it's a lot more work, it also seems beneficial
		in the long run -- testing will be easier, and the DEV program will
		be closer to the real thing. There's NO reason to rush into getting
		some kind of version of this completed...I've built a version before,
		so I already know I can do it. Now I just need to do it really well.
	"""

	# Get the correct class names from the ep = Event Prefix (passed in).
    eventUser_ClassName = ep + "_User"
    eventUser_Class = Object.factory(eventUser_ClassName)

    eventIxnR1_ClassName = ep + "R1"
    eventIxnR1_Class = Object.factory(eventIxnR1_ClassName)

    #
    # Create all other vars and lists needed.
    #

    # Calculate nums of stations and iPads from given parameters.
	s = m + mg
	i = s * 2

	# Make lists of station nums and iPad nums, to be rotated between subrounds.
	s_nums = list(x+1 for x in range(s))
	i_nums = list(x+1 for x in range(i))

	# Split the event user list into males and females; make enumeration useful
	# and list rotation between subrounds possible.
	li_males = li_eu[:m+mg]
	li_females = li_eu[m+mg:]

	# Initiate interaction counter and list-to-upload.
    counter_ixn = 0
    li_R1_obj_to_upload = []

    # Iterate through the subrounds.
    for j in range(s): # s = stations, and also subrounds, as used here

		for k, eu_obj in enumerate(li_males):
			# enumerator goes through the male half

    		counter_ixn += 1
		
    		new_ixn_object = eventIxnR1_Class(
    			ixNum = counter_ixn,
    			subNum = j + 1,
    			staNum = s_nums[]
	            user_objectId = eu_obj.objectId,
	            event_userNum = n + 1,
	            username = eu_obj.username,
	            sex = eu_obj.sex
    		)
    		li_R1_obj_to_upload.append(new_ixn_object)


























