"""

main_DEV.py

This program creates:

-  (DONE)  u _User objects with {create_u_Users_DEV.py}
-  (DONE)  g Ghost objects with {create_g_Ghosts_DEV.py}
-  (DONE)  i IPad objects with {create_i_IPads_DEV.py}
-  (DONE)  q Question objects with {create_q_Questions_DEV.py}
-          p zE0001_Player objects with {create_p_Players_DEV.py}
-          z zE####R1 objects with {create_z_R1_Interactions_DEV.py}

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
from my_own_modules_DEV.create_u_Users_DEV import create_u_users
from my_own_modules_DEV.create_g_Ghosts_DEV import create_g_ghosts
from my_own_modules_DEV.create_i_IPads_DEV import create_i_ipads
from my_own_modules_DEV.create_q_Questions_DEV import create_q_questions
from my_own_modules_DEV.create_zE0001_Players__DEV import create_event_players
#
### (simulate the event)
### from my_own_modules_DEV.create_zE****R1_DEV import create_r1_interactions
### from my_own_modules_DEV.create_zE****R2_DEV import create_r2_interactions
### from my_own_modules_DEV.create_zE****R3_DEV import create_r3_interactions
#
### (analyze the simulation)
### from my_own_modules_DEV.analyze_zE****R1__DEV import analyze_r1_interactions
### from my_own_modules_DEV.analyze_zE****R2__DEV import analyze_r2_interactions
### from my_own_modules_DEV.analyze_zE****R3__DEV import analyze_r3_interactions
### from my_own_modules_DEV.analyze_event__DEV import analyze_event
#
### (get other helper functions)
### from my_own_modules_DEV.get_event_class_name_DEV import get_event_class_name
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
        (can I do this here so I don't have to in every module?)
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
    i = 172
    q = 85

    # Call simulation setup functions.
    # create_u_users(u, m, f)
    # create_g_ghosts(g)
    # create_i_ipads(i)
    # create_q_questions(q)
    ep, mp, fp = create_event_players()

    sim_setup_end_time = time.time()
    sim_setup_total_time = round(sim_setup_end_time - program_start_time, 3)

    # Call event simulation and analysis functions.
    ### event_sim_start_time = time.time()
    ### create_r1_interactions()
    ### analyze_r1()
    ### create_r2_interactions()
    ### analyze_r2()
    ### create_r3_interactions()
    ### analyze_r3()
    ### analyze_event()
    total_number_of_setup_objects_uploaded = u + g + i + q + ep

    program_total_time = round(time.time() - program_start_time, 3)

    # Print execution times.
    print ("\
\n\n\
================================================\
\n\n\
Setting up the simulation took {} seconds to upload {} objects ({}/second).\
\n\n\
In total, program \"main__DEV.py\" took {} seconds.\
\n\n\
================================================\
\n\n\n\n\
".format(
    sim_setup_total_time,
    total_number_of_setup_objects_uploaded,
    round(total_number_of_setup_objects_uploaded / program_total_time, 3),
    program_total_time
    ))

###############################################################################

if __name__ == "__main__":
    main()










    ### THIS_EVENT_PLAYER_CLASS_NAME = "{}_Player".format(get_event_class_name())
    ### THIS_EVENT_R1_CLASS_NAME = "{}R1".format(get_event_class_name())
    ### create_AllParsePySubclassesOfObject(["_User", "Ghost", "IPad", "Question", THIS_EVENT_PLAYER_CLASS_NAME, THIS_EVENT_R1_CLASS_NAME])
   
























