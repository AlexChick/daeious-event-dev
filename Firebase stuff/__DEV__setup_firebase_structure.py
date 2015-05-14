"""

Set up an empty Firebase structure for see-again choice counts.
Looks like this:

"see-again-choices-zE0001R1": {

    "event_users": {
        
        "1": {
            "no": 12,
            "maybe-no": 1,
            "maybe-yes": 10,
            "yes": 4
        },

        "2": {
            "no": 2,
            "maybe-no": 5,
            "maybe-yes": 7,
            "yes": 13
        },    

        "3": { 
            "no": 8, 
            "maybe-no": 6,
            "maybe-yes": 3,
            "yes": 1
        }                  
    }
}
"""

"""



"""

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

# Import Firebase stuff (https://github.com/mikexstudios/python-firebase)
from firebase import Firebase
import requests

###############################################################################

def get_euns(eun):
	"""
	Returns a 4-character string with leading zeros as necessary.
		eun = event user number
		euns = event user number string
	"""
	return ("0" * (4 - len(str(eun)))) + str(eun)

###############################################################################

def main():
	"""
	"""

	root_reference = Firebase('https://burning-fire-8681.firebaseio.com')
	this_event_ref = root_reference.child('zE0001')
	R1_ref = this_event_ref.child('R1')
	R2_ref = this_event_ref.child('R2')
	R3_ref = this_event_ref.child('R3')

	for eun in range(1,11,1):
		for R_ref in [R1_ref, R2_ref, R3_ref]:
			eu_ref = R_ref.child("eu_{}".format(get_euns(eun)))
			eu_ref.put(
				{
				"n": random.randint(0,15),
				"mn": random.randint(0,15),
				"my": random.randint(0,15),
				"y": random.randint(0,15)
				}
			)

###############################################################################

if __name__ == "__main__":
	main()






























