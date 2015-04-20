
# Import Python stuff
import itertools
import math
import os
import random
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

	if 0 < eventNumber < 10:
		return "zE000{}".format(eventNumber)

	elif 10 <= eventNumber < 100:
		return "zE00{}".format(eventNumber)

	elif 100 <= eventNumber < 1000:
		return "zE0{}".format(eventNumber)

	elif 1000 <= eventNumber < 10000:
		return "zE{}".format(eventNumber)

	else:
		raise ValueError("eventNumber must be between 1 and 9999")