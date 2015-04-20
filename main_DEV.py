"""

main_DEV.py

This program creates:

-          u _User objects with {create_u_Users_DEV.py}
-          g Ghost objects with {create_g_Ghosts_DEV.py}
-  (DONE)  i IPad objects with {create_i_IPads_DEV.py}
-          q Question objects with {create_q_Questions_DEV.py}
-          p zE####_Player objects with {create_p_Players_DEV.py}
-          z zE####R1 objects with {create_z_R1_Interactions_DEV.py}

by importing their functions from the my_own_modules_DEV package inside the same directory.


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

# Import my custom stuff
###
### from my_own_modules_DEV.create_u_Users_DEV import create_u_users
### from my_own_modules_DEV.create_g_Ghosts_DEV import create_g_ghosts
from my_own_modules_DEV.create_i_IPads_DEV import create_i_ipads
from my_own_modules_DEV.create_q_Questions_DEV import create_q_questions
### from my_own_modules_DEV.create_p_Players_DEV import create_p_players
### from my_own_modules_DEV.create_z_R1_Interactions_DEV import create_z_r1_interactions
### from my_own_modules_DEV.get_event_class_name_DEV import get_event_class_name
###


def create_AllParsePySubclassesOfObject(list_of_classes_to_subclass):
    """
    * Creates Object subclasses for all Parse classes we're using.
    * 'list_of_classes_to_subclass' is a list of strings. 
    -- Do I need to do this if I'm making a subclass 
       for each class in their respective file?
                                                                    """
    l = list_of_classes_to_subclass[:]

    for className in list_of_classes_to_subclass:
        new_class = Object.factory(className)


def main():
    """ 
    * Start timer.
    * Call register() so ParsePy works.
    * Call all desired test functions.
    * Print total program running time.

    NOTE: Will fix to grab correct arguments from an object of class "Config" in Parse. 
    """

    # Start program timer.
    program_start_time = time.time()

    # Call "register" to allow parse_rest / ParsePy to work.
    # - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")


    # Call (or comment out) all desired "create" and "analyze" functions.
    ### create_u_users(134)
    ### create_g_ghosts(27)
    create_i_ipads(172)
    create_q_questions(55)
    ### create_p_players()
    ### create_r1_interactions()
    ### analyze_r1()
    ### create_r2_interactions()
    ### analyze_r2()
    ### create_r3_interactions()
    ### analyze_r3()
    ### analyze_event()

    # Print total program execution time.
    print "\
\n\n\
!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*\
\n\n\
Program \"main_DEV.py\" ran for {} seconds.\
\n\n\
!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*!@#$%^&*\
\n\
".format(round(time.time() - program_start_time, 3))




if __name__ == '__main__':
    main()






    ### THIS_EVENT_PLAYER_CLASS_NAME = "{}_Player".format(get_event_class_name())
    ### THIS_EVENT_R1_CLASS_NAME = "{}R1".format(get_event_class_name())
    ### create_AllParsePySubclassesOfObject(["_User", "Ghost", "IPad", "Question", THIS_EVENT_PLAYER_CLASS_NAME, THIS_EVENT_R1_CLASS_NAME])
   
























