from __future__ import print_function
"""
"""

###############################################################################
"""                                 IMPORTS                                 """
###############################################################################

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
### (Nothing to see here yet!)

###############################################################################
"""                                FUNCTIONS                                """
###############################################################################


def setup_event_users():
    """
    Create zE0001_User objects by "batch_save"-ing them to Parse using 
    ParsePy's ParseBatcher().  Player objects are _User objects whose 
    array_eventsRegistered contains 1.

    """

    # Start a function timer.
    function_start_time = time.time()

    class zE0001_User(Object):
        pass

    queryset_of_users_at_event = User.Query.filter(
        array_eventsRegistered__in = [1]
        )
    m_count = len(list(queryset_of_users_at_event.filter(sex = "M")))
    f_count = len(list(queryset_of_users_at_event.filter(sex = "F")))
    list_of_users_at_event = list(queryset_of_users_at_event)

    ep_count = len(list_of_users_at_event)

    list_of_ep_objects_to_upload = []

    for ep_num in range(ep_count):
        new_zE0001_User_object = zE0001_User(
            user_objectId = list_of_users_at_event[ep_num].objectId,
            playerNum = ep_num + 1,
            username = list_of_users_at_event[ep_num].username,
            sex = list_of_users_at_event[ep_num].sex
        )
        list_of_ep_objects_to_upload.append(new_zE0001_User_object)

    # Call batcher.batch_save on slices of the list no larger than 50.
    batcher = ParseBatcher()

    for k in range(ep_count/50 + 1):

        lo = 50*k
        hi = min(50*(k + 1), ep_count)

        batcher.batch_save(list_of_ep_objects_to_upload[lo:hi])

    # try:
    #     batcher.batch_save(list_of_ep_objects_to_upload[:])
    # except:
    #     batcher.batch_save(list_of_ep_objects_to_upload[0:50])
    #     batcher.batch_save(list_of_ep_objects_to_upload[50:ep_count])

    print ("\n{} zE0001_User objects uploaded to Parse in {} seconds.\n"
          .format(ep_count, round(time.time() - function_start_time, 2)))

    return ep_count, m_count, f_count

###############################################################################

def main():
    eu, mu, fu = setup_event_users()
    return "setup_event_users() has finished running.\
            There are {} people ({} men, {} women) at this event.\
            ".format(eu, mu, fu)

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)














