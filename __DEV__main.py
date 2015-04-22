"""

main_DEV.py

This program creates:

-  (DONE)  u _User objects
-  (DONE)  g Ghost objects
-  (DONE)  i IPad objects
-  (DONE)  q Question objects
-  (DONE)  eu zE0001_User objects

-          z1 zE0001_R1 objects
-          z2 zE0001_R2 objects
-          z3 zE0001_R3 objects


by importing their functions from the my_own_modules__DEV package inside the
same directory.


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

# Import my custom stuff
#
### (setup the simulation)
from packages.setup.__DEV__setup_Users import setup_users
from packages.setup.__DEV__setup_Ghosts import setup_ghosts
from packages.setup.__DEV__setup_IPads import setup_ipads
from packages.setup.__DEV__setup_Questions import setup_questions
from packages.setup.__DEV__setup_Event_Users import setup_event_users
#
### (prepare the pairings for each round)
### from packages.prepare.__DEV__prepare_R1 import prepare_R1
### from packages.prepare.__DEV__prepare_R2 import prepare_R2
### from packages.prepare.__DEV__prepare_R3 import prepare_R3
#
### (play each round)
### from packages.play.__DEV__play_R1 import play_R1
### from packages.play.__DEV__play_R2 import play_R2
### from packages.play.__DEV__play_R3 import play_R3
#
### (analyze the results of each round)
### from packages.analyze.__DEV__analyze_R1 import analyze_R1
### from packages.analyze.__DEV__analyze_R2 import analyze_R2
### from packages.analyze.__DEV__analyze_R3 import analyze_R3
### from packages.analyze.__DEV__analyze_event import analyze_event
#
### (get helper functions)
### from helpers.get_event_class_name import get_event_class_name
###

###############################################################################

# def create_AllParsePySubclassesOfObject(list_of_classes_to_subclass):
#     """
#     * Creates Object subclasses for all Parse classes we're using.
#     * 'list_of_classes_to_subclass' is a list of strings. 
#     -- Do I need to do this if I'm making a subclass 
#        for each class in their respective file?
#                                                                     """
#     l = list_of_classes_to_subclass[:]

#     for className in list_of_classes_to_subclass:
#         new_class = Object.factory(className)

###############################################################################

def main():
    """ 
    * Start timer.
    * Call register() so ParsePy works. 
    * Set all simulation setup parameter values.
    * Call all desired test functions.
    * Print total program running time.

    NOTE: Will fix to grab correct arguments (like eventNumber maybe?) from 
    an object of class "Config" in Parse. 
    """

    # Start program timer.
    program_start_time = time.time()

    # Call "register" to allow parse_rest / ParsePy to work. 
    # --> register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
        )

    # Set all simulation setup parameter values.
    u = 134
    m = 66
    f = 68
    g = 27
    i = 110
    q = 85

    # Call simulation setup functions.
    setup_users(u, m, f)
    setup_ghosts(g)
    setup_ipads(i)
    setup_questions(q)
    eu, mu, fu = setup_event_users()

    sim_setup_end_time = time.time()
    sim_setup_total_time = round(sim_setup_end_time - program_start_time, 2)

    # Call event simulation and analysis functions.
    ### event_sim_start_time = time.time()

    ### prepare_R1()
    ### play_R1
    ### analyze_R1()

    ### prepare_R2()
    ### play_R2()
    ### analyze_R2()

    ### prepare_R3()
    ### play_R3()
    ### analyze_R3()

    ### analyze_event()

    program_total_time = round(time.time() - program_start_time, 2)

    # Print execution times.
    print ("It took {} seconds for \"__DEV__main().py\" to run.\
    \nIt took {} seconds to upload {} objects (not counting users) ({}/second).\
    \nIt took ?.?? seconds to setup the event.\
    \n\
    \nIt took ?.?? seconds to prepare Round 1.\
    \nIt took ?.?? seconds to play Round 1.\
    \nIt took ?.?? seconds to analyze Round 1.\
    \n\
    \nIt took ?.?? seconds to prepare Round 2.\
    \nIt took ?.?? seconds to play Round 2.\
    \nIt took ?.?? seconds to analyze Round 2.\
    \n\
    \nIt took ?.?? seconds to prepare Round 3.\
    \nIt took ?.?? seconds to play Round 3.\
    \nIt took ?.?? seconds to analyze Round 3.\
    \n\
    \nIt took ?.?? seconds to analyze the event.\
    \n\n\n\n".format(
    program_total_time,
    sim_setup_total_time,
    g + i + q + eu,
    round((g + i + q + eu)/sim_setup_total_time, 2),
    ))

###############################################################################

if __name__ == "__main__":
    main()










    ### THIS_EVENT_PLAYER_CLASS_NAME = "{}_Player".format(get_event_class_name())
    ### THIS_EVENT_R1_CLASS_NAME = "{}R1".format(get_event_class_name())
    ### create_AllParsePySubclassesOfObject(["_User", "Ghost", "IPad", "Question", THIS_EVENT_PLAYER_CLASS_NAME, THIS_EVENT_R1_CLASS_NAME])
   
























