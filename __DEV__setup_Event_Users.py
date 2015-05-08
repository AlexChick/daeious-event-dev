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
#from __DEV__helpers_event import determine_ghosts_and_stations

###############################################################################
"""                                FUNCTIONS                                """
###############################################################################


def setup_event_users(m, f, mg, fg, ep):
    """
    Create zE0001_User objects by "batch_save"-ing them to Parse using 
    ParsePy's ParseBatcher(). Event User objects are _User objects whose 
    array_eventsRegistered contains the eventNum of this current event.

    """

    # Start a function timer.
    function_start_time = time.time()

    # Get the correct class name from the ep = Event Prefix (passed in).
    eventUser_ClassName = ep + "_User"
    eventUser_Class = Object.factory(eventUser_ClassName)

    # add some Users
    qset_all_users = User.Query.all().order_by("userNum")
    li_meu = list(qset_all_users.filter(sex = "M").limit(m))
    li_feu = list(qset_all_users.filter(sex = "F").limit(f))
    li_mgeu = list(qset_all_users.filter(sex = "MG").limit(mg))
    li_fgeu = list(qset_all_users.filter(sex = "FG").limit(fg))

    li_users_at_event = li_meu + li_feu + li_mgeu + li_fgeu

    count_eu = len(li_users_at_event)

    li_eu_obj_to_upload = []

    for n, eu_obj in enumerate(li_users_at_event):
        new_EU_object = eventUser_Class(
            user_objectId = eu_obj.objectId,
            event_userNum = n + 1,
            username = eu_obj.username,
            sex = eu_obj.sex
        )
        li_eu_obj_to_upload.append(new_EU_object)

    # # now add some ghosts
    # g, mg, fg, s = determine_ghosts_and_stations(meu_count, feu_count)
    # qset_all_ghosts = User.Query.filter(userNum__gte = 1000000).order_by("userNum")
    # list_male_ghosts = list(qset_all_ghosts.filter(userNum__lte = 1000007))[:mg]
    # list_female_ghosts = list(qset_all_ghosts.filter(userNum__gte = 1000006))[:fg]
    # list_ghosts_at_event = list_male_ghosts + list_female_ghosts
    # print (len(list_ghosts_at_event))
    # print (len(list_male_ghosts))
    # print (len(list_female_ghosts))
    # print (list_ghosts_at_event)
    # print (list_male_ghosts)
    # print (list_female_ghosts)
    # print (g)

    # for gu_num in range(g):
    #     new_Event_User_object = zE0001_User(
    #         user_objectId = list_ghosts_at_event[gu_num].objectId,
    #         event_userNum = gu_num + 100 + 1,
    #         username = list_ghosts_at_event[gu_num].username,
    #         sex = list_ghosts_at_event[gu_num].sex
    #         )
    #     list_of_eu_objects_to_upload.append(new_Event_User_object)


    # Call batcher.batch_save on slices of the list no larger than 50.
    batcher = ParseBatcher()

    for k in range(count_eu/50 + 1):

        lo = 50*k
        hi = min(50*(k + 1), count_eu)
        batcher.batch_save(li_eu_obj_to_upload[lo:hi])


    print ("\n{} zE0001_User objects uploaded to Parse in {} seconds.\n"
          .format(count_eu, round(time.time() - function_start_time, 2)))

    return li_eu_obj_to_upload

###############################################################################

def main():
    li = setup_event_users(m, f, mg, fg, ep)
    return "setup_event_users() has finished running.\
            There are {} people - {} men, {} women, {} male ghosts\
             and {} female ghosts ({} total users) - at this event.\
            ".format(m,f,mg,fg,count_eu)

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)














