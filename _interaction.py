from __future__ import print_function # apparently, has to be on first line

"""
This program begins with an empty Parse database and
simulates a Daeious event from start to finish.
"""

###############################################################################
"""                                 IMPORTS                                 """
###############################################################################

# Import Python stuff.

from pprint import pprint
import itertools
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
from helpers import batch_delete_from_Parse
from helpers import batch_delete_from_Parse_all_objects_of_class
from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import fetch_object_from_Parse_of_class
from helpers import register_with_Parse



###############################################################################
"""                                 GLOBALS                                 """
###############################################################################

NUM_STATIONS = 0

###############################################################################
"""                                 CLASSES                                 """
###############################################################################

class Interaction(Object): pass # needed for Parse Event class interactivity

###############################################################################

class _Interaction(Object):

	CURRENT_IX_NUM = 0

	def __init__(self):

		#Increment the current ix_num
		_Interaction.CURRENT_IX_NUM += 1

		self.ix_num = _Interaction.CURRENT_IX_NUM
		self.sub_num = None
		self.sta_num = None
		self.m_event_user_num = None
		self.f_event_user_num = None
		self.m_username = None
		self.f_username = None
		self.m_user_object_id = None
		self.f_user_object_id = None
		self.m_event_user_object_id = None
		self.f_event_user_object_id = None
		self.m_ipad_num = None
		self.f_ipad_num = None
		self.q_num = None

		# fill in all those blanks
		#self.fill_in_info()

		pass

	def simulate(self):
		# Generate QA and SAC, and save them in the right place in Firebase.
		pass
		

	pass

###############################################################################

###############################################################################
"""                                  MAIN                                   """
###############################################################################


def main():
	register_with_Parse()
	# creates 150 _Interactions objects, then batch uploads them to Parse
	li = []
	for i in range(150):
		ix = _Interaction()
		pix = Interaction()
		pix.ixNum = ix.ix_num
		li.append(pix)
	batch_upload_to_Parse("Interaction", li)
	print(ix.ix_num)

	pass

if __name__ == '__main__':
    status = main()
    sys.exit(status)













