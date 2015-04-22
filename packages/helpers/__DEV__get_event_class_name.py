"""
"""

# Import Python stuff
import itertools
import math
import os
import random
import sys
import time
from pprint import pprint

# Import Parse stuff
import httplib, json, urllib

# Import ParsePy stuff
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

def get_event_class_name(eventNumber = 1):

	""" Currently takes an argument, but retrieving the correct eventNumber
		will (eventually) be part of the function.
	"""
	event_class_name = None

	if 0 < eventNumber < 10:
		event_class_name = "zE000{}".format(eventNumber)

	elif 10 <= eventNumber < 100:
		event_class_name = "zE00{}".format(eventNumber)

	elif 100 <= eventNumber < 1000:
		event_class_name = "zE0{}".format(eventNumber)

	elif 1000 <= eventNumber < 10000:
		event_class_name = "zE{}".format(eventNumber)

	else:
		raise ValueError("eventNumber must be between 1 and 9999")

	print "\nTHIS_EVENT_CLASS_NAME: {}\n".format(event_class_name)

	return event_class_name