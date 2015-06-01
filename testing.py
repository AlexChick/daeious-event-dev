# Import Python stuff.
from __future__ import print_function # apparently, has to be on first line
from pprint import pprint
import itertools
import logging
import math
import os
import random
import sys
import time

# Import stuff that Parse might use.
import httplib, json, urllib

# Import ParsePy stuff. ParsePy makes using Parse in Python much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Import Firebase stuff (https://github.com/mikexstudios/python-firebase)
from firebase import Firebase
import requests

# Import custom functions and classes I've written specifically for Daeious.
import daeious
from helpers import batch_delete_from_Parse
from helpers import batch_delete_from_Parse_all_objects_of_class
from helpers import batch_query
from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import fetch_object_from_Parse_of_class
from helpers import mk_serial
from helpers import register_with_Parse

import backoff

register_with_Parse()



# Logging

# # define a Handler which writes ERROR messages or higher to the sys.stderr
# console = logging.StreamHandler()
# # set up logging to file - see previous section for more details
# logging.basicConfig(level=logging.ERROR,
#                     #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%m-%d %H:%M',
#                     filename='',
#                     filemode='w')
# # set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# # tell the handler to use this format
# console.setFormatter(formatter)
# # add the handler to the root logger
# #logging.getLogger('').addHandler(console)
logging.getLogger('').addHandler(logging.StreamHandler())

#logging.error("\n\n\n\n\n      (Oops! Too many requests to Parse again!)\n\n\n\n\n")

################################################################################
################################################################################
################################################################################

li_times = []

for i in range(1):
	li_times.append(daeious.main())

print (li_times)
print ("\nAverage time: {}\n".format(sum(li_times)/len(li_times)))








# EVENT_NUMBER = 98

# class Event(object):
# 	print EVENT_NUMBER, 1
# 	global EVENT_NUMBER # allows access to EVENT_NUMBER inside print_this().
# 	EVENT_NUMBER = 0
# 	print EVENT_NUMBER, 2
# 	EVENT_NUMBER += 1
# 	print EVENT_NUMBER, 3
# 	a = 0

# 	def __init__(self):
# 		Event.a += 1
# 		print Event.a
# 		self.eNum = EVENT_NUMBER

# 	def print_this(self):
# 		print self.eNum, 5
# 		print EVENT_NUMBER, 6
# 		EVENT_NUMBER += 1
# 		print EVENT_NUMBER, 7

# class Event():

# 	global MEN
# 	global WOMEN
# 	global START_AT_ROUND
# 	MEN = 7
# 	WOMEN = 9
# 	START_AT_ROUND = 0

# 	def __init__(self, men = 20, women = 25):

# 		#print MEN, WOMEN, 1
# 		print men, women, 4
# 		#MEN += 1
# 		#print MEN, WOMEN, 2
# 		self.men = men
# 		self.women = women
# 		self.something = MEN
		
# 		#self.MEN = MEN + 2
# 		#self.WOMEN = WOMEN + 2
# 		#print self.MEN, self.WOMEN, 3

# 		START_AT_ROUND = 5

# 	def do_something(self):
# 		print MEN, WOMEN, 19



# e = Event()
# print e.men, e.something, START_AT_ROUND


# from itertools import cycle
# from time import sleep
# import sys

# myList = range(1, 5 + 1) # [1, 2, 3, ..., 19, 20, 21]

# myCycle = cycle(myList)

# for n in myList:
# 	for item in myCycle:
# 		sys.stdout.write("{}{}".format(" "*(item-1), item))
# 		sys.stdout.flush()
# 		sleep(1)
# 	myCycle = cycle([myList[-1]] + myList[:-1])





































