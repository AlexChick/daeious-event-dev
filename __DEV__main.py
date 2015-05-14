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

# Import my custom stuff
#
### (setup the simulation)
from __DEV__setup_Users import setup_users
from __DEV__setup_Ghosts import setup_ghosts
from __DEV__setup_IPads import setup_ipads
from __DEV__setup_Questions import setup_questions
from __DEV__setup_Event_Users import setup_event_users
#
### (prepare the pairings for each round)
from __DEV__prepare_R1 import prepare_R1
### from __DEV__prepare_R2 import prepare_R2
### from __DEV__prepare_R3 import prepare_R3
#
### (play each round)
### from __DEV__play_R1 import play_R1
### from __DEV__play_R2 import play_R2
### from __DEV__play_R3 import play_R3
#
### (analyze the results of each round)
### from __DEV__analyze_R1 import analyze_R1
### from __DEV__analyze_R2 import analyze_R2
### from __DEV__analyze_R3 import analyze_R3
### from __DEV__analyze_event import analyze_event
#
### (get helper functions)
# from __DEV__helpers_event import create_event_object
from __DEV__helpers_event import determine_ghosts_and_stations
from __DEV__helpers_event import get_this_event_num
from __DEV__helpers_event import make_event_prefix
# from __DEV__helpers_event import EVENT_DATE
# from __DEV__helpers_event import EVENT_TIME
# from __DEV__helpers_event import EVENT_LOCATION
###


# VARS

EVENT_NUM = get_this_event_num()
EVENT_PREFIX = make_event_prefix(EVENT_NUM)

EVENT_DATE = time.strftime("%Y.%m.%d")
EVENT_TIME = random.choice(["19:00", "19:30", "20:00", "20:30", "21:00"])
EVENT_LOCATION = random.choice(["Palo Alto", "San Francisco", "Los Angeles"])

M_U = random.randint(20,50)
F_U = 0
while abs(M_U - F_U) > 5:
    F_U = random.randint(20,50)

# comment these 2 lines out when setting it back to random # of people
M_U = 20
F_U = 20

M_G = 0
F_G = 0

M_I = 0
F_I = 0

U_G = 0
S = 0

U_G, M_G, F_G, S = determine_ghosts_and_stations(M_U, F_U)
M_I = S
F_I = S




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
    # Create event object.
    * Set all simulation setup parameter values.
    * Call all desired test functions.
    * Print total program running time.

    NOTE: Will fix to grab correct arguments (like eventNumber maybe?) from 
    an object of class "Config" in Parse. 
    """

    # Call "register" to allow parse_rest / ParsePy to work. 
    # --> register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
        )

    class Event(Object):
        pass

    # EVENT_NUM = get_this_event_num()
    # EVENT_PREFIX = make_event_prefix(EVENT_NUM)

    #e = create_event_object()

    e = Event(
        eventNum = EVENT_NUM,
        eventPrefix = EVENT_PREFIX,
        location = EVENT_LOCATION,
        startDate = EVENT_DATE,
        startTime = EVENT_TIME,
        start = [EVENT_DATE, EVENT_TIME],
        numMen = M_U,
        numWomen = F_U,
        numUsers = M_U + F_U,
        numMaleGhosts = M_G,
        numFemaleGhosts = F_G,
        numUserGhosts = U_G,
        numStations = S,
        numIPads = 2 * S

        )

    e.save()

    # # Set all simulation setup parameter values.
    # u = 134
    # m = 66
    # f = 68
    # g = 27
    # i = 110
    # q = 85

    # Call simulation setup functions.
    #setup_users(u, m, f)
    #setup_ghosts(g)
    #setup_ipads(i)
    #setup_questions(q)
    li_event_users = setup_event_users(M_U, F_U, M_G, F_G, EVENT_PREFIX)
    # e.numMen = M_U
    # e.numWomen = F_U
    # e.numUsers = M_U + F_U
    #eg, emg, efg, es = determine_ghosts_and_stations(mu, fu)
    # e.numGhosts = U_G
    # e.numMaleGhosts = M_G
    # e.numFemaleGhosts = F_G
    # e.numStations = S
    # e.numMaleIPads = S
    # e.numFemaleIPads = S


    # Call event simulation and analysis functions.

    prepare_R1(M_U, F_U, M_G, F_G, EVENT_PREFIX, li_event_users)
    ### play_R1
    ### analyze_R1()

    ### prepare_R2()
    ### play_R2()
    ### analyze_R2()

    ### prepare_R3()
    ### play_R3()
    ### analyze_R3()

    ### analyze_event()


    # # Print execution times.
    # print ("It took {} seconds for \"__DEV__main().py\" to run.\
    # \nIt took {} seconds to upload {} objects (not counting users) ({}/second).\
    # \nIt took ?.?? seconds to setup the event.\
    # \n\
    # \nIt took ?.?? seconds to prepare Round 1.\
    # \nIt took ?.?? seconds to play Round 1.\
    # \nIt took ?.?? seconds to analyze Round 1.\
    # \n\
    # \nIt took ?.?? seconds to prepare Round 2.\
    # \nIt took ?.?? seconds to play Round 2.\
    # \nIt took ?.?? seconds to analyze Round 2.\
    # \n\
    # \nIt took ?.?? seconds to prepare Round 3.\
    # \nIt took ?.?? seconds to play Round 3.\
    # \nIt took ?.?? seconds to analyze Round 3.\
    # \n\
    # \nIt took ?.?? seconds to analyze the event.\
    # \n\n\n\n".format(
    # program_total_time,
    # sim_setup_total_time,
    # g + i + q + eu,
    # round((g + i + q + eu)/sim_setup_total_time, 2),
    # ))

###############################################################################

if __name__ == "__main__":
    main()










    ### THIS_EVENT_PLAYER_CLASS_NAME = "{}_Player".format(get_event_class_name())
    ### THIS_EVENT_R1_CLASS_NAME = "{}R1".format(get_event_class_name())
    ### create_AllParsePySubclassesOfObject(["_User", "Ghost", "IPad", "Question", THIS_EVENT_PLAYER_CLASS_NAME, THIS_EVENT_R1_CLASS_NAME])
   
























