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
# Since this is main, I'm importing everything as a kind of reference to all
#   the custom classes and helpers functions available, but I don't think
#   that it's necessary to import all of them here.
from _event import _Event
from _round import _Round, Round_0, Round_1, Round_2, Round_3, Round_4
from helpers import batch_delete_from_Parse
from helpers import batch_delete_from_Parse_all_objects_of_class
from helpers import batch_upload_to_Parse
from helpers import create_QA_database_in_Firebase
from helpers import create_SAC_database_in_Firebase
from helpers import fetch_object_from_Parse_of_class
from helpers import register_with_Parse

###############################################################################
"""                                FUNCTIONS                                """
###############################################################################

def main():
    """
    1. Register with Parse.
    2. Create an empty class matching each class in Parse.
    3. Delete existing Event objects from Parse.
    4. Delete existing Round objects from Parse.
    5. Delete existing event-user objects (zE0000_User) from Parse.
    6. Delete existing interaction objects (zE0000_R1, etc.) from Parse.
    """



    # 1. Register with Parse.
    register_with_Parse()


    # 2. Create an empty class matching each class in Parse.
    # (Might not be necessary...but is a good reference list)
    # (I tried to put this in a function, but couldn't get it to work - yet.)
        # event-specific classes
    class zE0000_User(Object): pass
    class zE0000R1_Ix(Object): pass
    class zE0000R2_Ix(Object): pass
    class zE0000R3_Ix(Object): pass
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


    ## Delete existing event-specific objects from Parse 
    ## to maintain sanity when testing
    ## (The for: loop should work too, but if I want to save time when testing,
    ## I can comment out individual lines, so that's how I've kept them)
    # for cls in ["Event", "Round", "zE_0000_User", "zE_0000_R1", "zE_0000_R2", 
    # "zE_0000_R3"]:
    #     batch_delete_from_Parse_all_objects_of_class(cls)

    batch_delete_from_Parse_all_objects_of_class("Event")
    batch_delete_from_Parse_all_objects_of_class("Round")
    batch_delete_from_Parse_all_objects_of_class("zE0000_User")
    batch_delete_from_Parse_all_objects_of_class("zE0000R1_Ix")
    batch_delete_from_Parse_all_objects_of_class("zE0000R2_Ix")
    batch_delete_from_Parse_all_objects_of_class("zE0000R3_Ix")


    # Simulate event

    # 1. Create an _Event object.
    e = _Event(0, 50, 50)

    # 2. .simulate the entire event.
    e.simulate()

    # 3. Run tests on the results.

    pass


###############################################################################
"""                                  MAIN                                   """
###############################################################################

if __name__ == '__main__':
    status = main()
    print("Event simulation complete.")
    sys.exit(status)














