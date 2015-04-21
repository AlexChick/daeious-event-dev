"""
"""

# Import Python stuff
from __future__ import print_function
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
### from my_own_modules.decorator_asterisk import decorate_prints_with_asterisks
###

###########################
###########################

def create_event_players():
    """
    Create zE0001_Player objects by "batch_save"-ing them to Parse using 
    ParsePy's ParseBatcher().  Player objects are _User objects whose 
    array_eventsRegistered contains 1.

    """

    # Start a function timer.
    function_start_time = time.time()

    # Calling "register" allows parse_rest / ParsePy to work.
    # - register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register("AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
             "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
             master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv")

    class zE0001_Player(Object):
        pass

    queryset_of_users_at_event = User.Query.filter(
        array_eventsRegistered__in = [1]
        )
    m_count = len(list(queryset_of_users_at_event.filter(sex = "M")))
    f_count = len(list(queryset_of_users_at_event.filter(sex = "F")))
    list_of_users_at_event = list(queryset_of_users_at_event)

    list_of_event_player_objects_to_upload = []

    ep_count = len(list_of_event_player_objects_to_upload)

    for ep_num in range(1, ep_count + 1, 1):
        new_zE0001_Player_object = zE0001_Player(
            user_objectId = list_of_users_at_event[ep_num].objectId,
            playerNum = ep_num,
            username = list_of_users_at_event[ep_num].username,
            sex = list_of_users_at_event[ep_num].sex
        )
        list_of_event_player_objects_to_upload.append(new_Ghost_object)

    batcher = ParseBatcher()

    # Call batcher.batch_save on slices of the list no larger than 50.
    for k in range(ep_count/50 + 1):
        ### lower = 50*k
        ### upper = 
        try:
            batcher.batch_save(list_of_event_player_objects_to_upload[
                50*k : 50*(k + 1)
                ])
        except:
            batcher.batch_save(list_of_event_player_objects_to_upload[
                50*k : ep_count
                ])

    try:
        batcher.batch_save(list_of_event_player_objects_to_upload[:])
    except:
        batcher.batch_save(list_of_event_player_objects_to_upload[0:50])
        batcher.batch_save(list_of_event_player_objects_to_upload[50:ep_count])

    batcher.batch_save(list_of_event_player_objects_to_upload)

    print ("\n{} zE0001_Player objects uploaded to Parse in {} seconds.\n"
          .format(ep_count, round(time.time() - function_start_time, 3)))

    return ep_count, m_count, f_count

###########################
###########################

def main():
    ep, m, f = create_event_players()
    return "create_event_players() has finished running.\
            There are {} people ({} men, {} women) at this event.\
            ".format(ep, m, f)

if __name__ == '__main__':
    status = main()
    sys.exit(status)














