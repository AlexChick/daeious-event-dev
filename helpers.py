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

def mk_serial(eNum):
    return "{}{}".format("0"*(4 - len(str(eNum))), eNum)


def register_with_Parse():
    # Call "register(?,?,?)" to allow parse_rest / ParsePy to work. 
    # register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
    )
    pass


def batch_delete_from_Parse_all_objects_of_class(str_cls_name):
    # Parse's default limit for query results is 100, and max is 1000,
    # but each query has to be set that way. I should extend this
    # function to query more than 1000.
    #
    # Fixed; now sleeps for (hi-lo)/30 seconds instead of 50/30 = 1.67 seconds.

    # Query for all objects of the passed-in class name.
    cls = Object.factory(str_cls_name)
    all_objects_to_delete = list(cls.Query.all().limit(1000))
    num_to_del = cls.Query.all().limit(1000).count()
    num_deleted = 0

    print("\n(deleting {} {} objects from Parse)".format(num_to_del, str_cls_name))

    # for some reason, cls.Query.all() is only returning 100 results,
    # so just keep querying until there's nothing left.
    while True: 

        # Return if there aren't any existing objects of that class
        if num_deleted == num_to_del:
            return

        # Then, batch delete them.
        batcher = ParseBatcher()

        for x in range((num_to_del-1)/50 + 1):
            lo = 50*x
            hi = min(50*(x+1), num_to_del)
            if lo == hi:
                return
            batcher.batch_delete(all_objects_to_delete[lo:hi])
            num_deleted += hi - lo

            sys.stdout.write("\r{} of {} old {}'s deleted ({}{})".format(
                min(50 + (50*x), num_to_del),
                num_to_del,
                str_cls_name,
                min(int(round((50*(x+1)*100.0)/num_to_del, 0)), 100),
                "%"
                ))
            sys.stdout.flush() # must be done for it to work (why?)
            time.sleep((hi-lo)/30.0) # explained above

        sys.stdout.write("\n") # move cursor to the next line after we're done





    pass


def batch_upload_to_Parse(Parse_class_name, li_objects):
    # avoids timeout when batch uploading / saving.

    # Save multiple objects to Parse.
    # Call batcher.batch_save on slices of the list no larger than 50.
        # (Parse will timeout if 1800 requests are made in 60 seconds,
        # hence the time.sleep((hi-lo)/30.0) every run of objects saved.)

    batcher = ParseBatcher()

    num_to_up = len(li_objects)

    print("\n(uploading {} {} objects to Parse)".format(num_to_up, Parse_class_name))

    for x in range((num_to_up-1)/50 + 1):
        batcher = ParseBatcher()
        lo = 50*x
        hi = min(50 * (x+1), num_to_up)

        batcher.batch_save(li_objects[lo:hi])

        sys.stdout.write("\r{} of {} new {}'s uploaded ({}{})".format(
            min(50 + (50*x), num_to_up), 
            num_to_up,
            Parse_class_name,
            min(int(round((50*(x+1)*100.0)/num_to_up, 0)), 100),
            "%"
            ))
        sys.stdout.flush() # must be done for it to work (why?)
        time.sleep((hi-lo)/30.0) # explained above

    sys.stdout.write("\n") # move the cursor to the next line after we're done

    pass





def batch_query(
                Source, 
                Cls, 
                Filter = [None, None, None], 
                Limit = 1000, 
                OrderBy = None, 
                Skip = 0
                ):

    if Source == "Parse":

        # if Cls == User:
        #     q = User.Query.all().limit(Limit)
        # else:
        #     q = Cls.Query.all().limit(Limit)
        q_start = time.time()

        if Filter == [None, None, None]:
            q = Cls.Query.all().limit(Limit).skip(Skip)
        else:
            f = Filter[0]
            op = Filter[1]
            val = Filter[2]        
            if f == "sex" and op == "=":
                q = Cls.Query.all().filter(sex = val).limit(Limit).skip(Skip)
            if f == "qNum" and op == "<=":
                q = Cls.Query.all().filter(qNum__lte = val).limit(Limit).skip(Skip)

        len_q = len(q)

        q_time_taken = time.time() - q_start
        q_time_taken = 0

        print("\n(Sleeping for {} seconds after {} {} objects were batch queried from Parse)"\
            .format(round(len_q/30.0 - q_time_taken, 2), len_q, Cls.__name__)
            )
        time.sleep(len_q/30.0 - q_time_taken)

        if OrderBy != None:
            q.order_by(OrderBy)

        return q

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


###############################################################################
"""                                  MAIN                                   """
###############################################################################


def main():
    register_with_Parse()
    batch_delete_from_Parse_all_objects_of_class("Event")
    batch_delete_from_Parse_all_objects_of_class("zE0000_User")
   # batch_upload_to_Parse()
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





