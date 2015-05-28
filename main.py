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
from event import _Event
from _round import _Round, Round_0, Round_1, Round_2, Round_3, Round_4
from helpers import batch_delete_from_Parse
from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import delete_all_z_E0000_R1_objects_from_Parse
from helpers import fetch_object_from_Parse_of_class
from helpers import register_with_Parse

###############################################################################
"""                                FUNCTIONS                                """
###############################################################################

def main():


    # Register with Parse.
    register_with_Parse()


    # Connect with Parse classes.
        # (I tried to put this in a function, but couldn't get it to work)

        # event-specific classes
    class z_E0000_R1(Object): pass
    class z_E0000_User(Object): pass

        # general classes
    class Config(Object): pass
    class Employee(Object): pass
    class Event(Object): pass
    class Ghost(Object): pass
    class Interaction(Object): pass
    class IPad(Object): pass
    class Question(Object): pass
    class Round(Object): pass
    class Test_Class(Object): pass    


    # Delete existing z_E0000_R1 objects from Parse
    delete_all_z_E0000_R1_objects_from_Parse()


    # Simulate event
    e = _Event(0, 50, 50)
    e.simulate()


    pass


###############################################################################
"""                                  MAIN                                   """
###############################################################################

if __name__ == '__main__':
    status = main()
    print("Event simulation complete.")
    sys.exit(status)














