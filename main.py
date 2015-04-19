"""

main.py

This program:

- creates u _User objects with {create_n__Users_DEV.py} (double underscore in there)
- creates g Ghost objects with {create_g_Ghosts_DEV.py}
- creates i IPad objects with {create_i_IPads_DEV.py}
- creates q Question objects with {create_q_Questions_DEV.py}
- creates p zE####_Player objects with {create_p_Players_DEV.py}
- creates z zE####R1 objects with {create_z_R1_Interactions_DEV.py}

... by importing their functions.


"""


# import general stuff
import itertools, math, os, random, time # python stuff
import json, httplib, urllib # parse stuff
from pprint import pprint # pretty printing
# import ParsePy stuff
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User
# import my custom stuff
from create_i_IPads_DEV import create_i_ipads
###
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
    * Starts timer
    * Calls register() so ParsePy works
    * Calls all desired test functions
    * Prints total program running time

        -- Will fix to grab correct numbers from an object of class "Config" in Parse. 


                                                                    """

    # start program timer
    program_start_time = time.time()

    # Calling "register" allows parse_rest / ParsePy to work.
    # - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")

    # Call (or comment out) all desired functions here.
    create_AllParsePySubclassesOfObject(["_User", "Ghost", "IPad", "Question"])
    create_i_ipads(200)

    # print total program running time
    print "\n\nProgram complete. Total time taken: {} seconds.\n".format(round(time.time() - program_start_time, 3))



main()































