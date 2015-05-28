"""
The Round class has methods for simulating and analyzing a round.

Also included are 5 subclasses: Round_1, Round_2, Round_3, Round_4, Round_5.
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

# Import Firebase stuff (https://github.com/mikexstudios/python-firebase)
from firebase import Firebase
import requests

# Import custom functions and classes I've written specifically for Daeious.
from helpers import register_with_Parse
###############################################################################

register_with_Parse()


class Round(Object): pass

class _Round(Object):

    EVENT_NUM = -1
    CURRENT_ROUND = -1

    def __init__(self):

    	# Increment the current round.
    	_Round.CURRENT_ROUND += 1

    	# Create a Round object in Parse and upload it.
    	self.r = Round()
    	self.r.roundNum = _Round.CURRENT_ROUND
    	self.r.save()

    	# Initialize the round_num variable
    	self.round_num = None

    	pass

    def prepare(self):
    	pass

    def simulate(self):
    	pass

    def analyze(self):
    	pass
        

class Round_0(_Round):
	"""
	Pregame stuff. Assume sufficient (>100) Users exist in Parse.
	"""

	def __init__(self):
		_Round.__init__(self)
		self.round_num = 0
		print(self.r.roundNum)
		print(self.round_num)
		pass

	def create_event_users_in_Parse(self):
		pass

	pass


class Round_1(_Round):
	pass


class Round_2(_Round):
	pass


class Round_3(_Round):
	pass


class Round_4(_Round):
	"""
	Postgame stuff.
	"""

	pass



###############################################################################
"""                                  MAIN                                   """
###############################################################################

def main():

	r0 = Round_0()
	r0test = Round_0()
	print (r0.r)
	print (_Round.CURRENT_ROUND)

if __name__ == '__main__':
    status = main()
    sys.exit(status)













