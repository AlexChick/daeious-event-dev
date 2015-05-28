from __future__ import print_function # has to be on first line or throws error

"""
This program contains several helpful little functions.
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

###############################################################################
"""                                FUNCTIONS                                """
###############################################################################


def fetch_object_from_Parse_of_class(SomeClass):
    pass


def register_with_Parse():
    # Call "register(?,?,?)" to allow parse_rest / ParsePy to work. 
    # register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
    )
    pass


def batch_delete_from_Parse_all_objects_of_class(classname):

    while True: # for some reason, batch_delete is only 
        # Query for all objects of the passed-in class name.
        myClassName = classname
        myClass = Object.factory(myClassName)
        all_objects_to_delete = list(myClass.Query.all())
        print("About to delete {} objects.".format(len(all_objects_to_delete)))

        # Then, batch delete them.
        batcher = ParseBatcher()
        li_length = len(all_objects_to_delete)
        print ("li_length: {}".format(li_length))

        if li_length == 0:
            return # no objects to delete, or we're done

        for x in range(li_length/50 + 1):

            lo = 50*x
            hi = min(50 * (x+1), li_length)
            batcher.batch_delete(all_objects_to_delete[lo:hi])

            sys.stdout.write("\r{} of {} old {}'s deleted ({}{})".format(
                50 + (50*x), 
                li_length,
                classname,
                int(round((50*(x+1)*100.0)/li_length, 0)), 
                "%"
                ))
            sys.stdout.flush() # must be done for it to work (why?)
            time.sleep(1.67) # explained above

        sys.stdout.write("\n") # move the cursor to the next line after we're done





    pass


def batch_upload_to_Parse(Parse_class_name, li_objects):
    # avoids timeout when batch uploading / saving.

    # Save multiple objects to Parse.
    # Call batcher.batch_save on slices of the list no larger than 50.
        # (Parse will timeout if 1800 requests are made in 60 seconds,
        # hence the time.sleep(1.67) every 50 objects saved.)

    batcher = ParseBatcher()

    li_length = len(li_objects)

    for x in range(li_length/50 + 1):
        lo = 50*x
        hi = min(50 * (x+1), li_length)
        batcher.batch_save(li_objects[lo:hi])

        sys.stdout.write("\r{} of {} new {}'s uploaded ({}{})".format(
            50 + (50*x), 
            li_length,
            Parse_class_name,
            int(round((50*(x+1)*100.0)/li_length, 0)), 
            "%"
            ))
        sys.stdout.flush() # must be done for it to work (why?)
        time.sleep(1.67) # explained above

    sys.stdout.write("\n") # move the cursor to the next line after we're done

    pass


def batch_delete_from_Parse(Parse_class_name, li_objects):
    # avoids timeout
    pass


def create_QA_database_in_Firebase(create_QA):

    if create_QA:
        pass

    pass


def create_SAC_database_in_Firebase(create_SAC):
    
    if create_SAC:
        pass

    pass
    # Create see-again-choice data-holding structure in Firebase.
    # Looks like:

    #     "see-again-choices-zE0001R1": {

            #     "event_users": {
                    
            #         "1": {
            #             "no": 12,
            #             "maybe-no": 1,
            #             "maybe-yes": 10,
            #             "yes": 4
            #         },

            #         "2": {
            #             "no": 2,
            #             "maybe-no": 5,
            #             "maybe-yes": 7,
            #             "yes": 13
            #         },    

            #         "3": { 
            #             "no": 8, 
            #             "maybe-no": 6,
            #             "maybe-yes": 3,
            #             "yes": 1
            #         },

            #         ...           
            #     }
            # }


def main():
    register_with_Parse()
    batch_delete_from_Parse_all_objects_of_class("Event")
    batch_delete_from_Parse_all_objects_of_class("zE_0000_User")
    pass

if __name__ == "__main__":
    status = main()
    print("\nTesting complete for helpers.py\n")
    sys.exit(status)

















# def connect_with_Parse_classes():


#     # event-specific classes

#     class z_E0000_R1(Object): pass

#     class z_E0000_User(Object): pass

#     # general classes

#     class Config(Object): pass

#     class Employee(Object): pass
 
#     class Event(Object): pass

#     class Ghost(Object): pass

#     class Interaction(Object): pass

#     class IPad(Object): pass

#     class Question(Object): pass

#     class Round(Object): pass

#     class Test_Class(Object): pass

#     pass





