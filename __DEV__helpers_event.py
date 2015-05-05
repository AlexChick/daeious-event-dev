"""
(I need some kind of logic that fills in numMen, numGhosts, et cetera.)

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

EVENT_DATE = ""
EVENT_TIME = ""
EVENT_LOCATION = ""


###############################################################################

def create_event_object(this_date, this_time, this_location):
    """
    Create an Event object, upload it to Parse, return e.
 
    this_date has format "YYYY.MM.DD"
    this_time has format "HH:MM" (24-hour clock)
    this_location is a string (ex, "Palo Alto")
    """

    class Event(Object):
        pass

    EVENT_DATE = this_date
    EVENT_TIME = this_time
    EVENT_LOCATION = this_location


    en = get_this_event_num()
    p = make_event_prefix(en)

    e = Event(
        eventNum = en,
        eventPrefix = p,
        location = EVENT_LOCATION,
        startDate = EVENT_DATE,
        startTime = EVENT_TIME,
        start = [this_date, this_time]
        )

    e.save()

    print "\nSuccessfully created Daeious Event #{}, {}.\n".format(en, p)

    return e

###############################################################################

def determine_ghosts_and_stations(m, f):
    """
    Determine how many ghosts, which lets us know how many stations too.
    This code can probably be significantly cleaned up, but right now I'm just
    gonna get it written.

    A single ghost always goes to the min(m,f).

    m, f must each be >= 20 and <= 50.
    abs(m-f) must be <= 5 (might be low, we'll see).

    """

    if not ((20 <= m <= 50) and (20 <= f <= 50) and (abs(m-f) <= 5)):
        raise ValueError("m and f must be between 20 and 50 inclusive, and \
            they must differ by no more than 5.")

    g = -1
    s = -1

    # if diff is 0:
    if m == f:
        if m%2 == 0: # both even
            g = 0
            s = m
        else: # both odd
            g = 2 #(1 each)
            s = m + 1

    # if diff is 1:
    elif abs(m-f) == 1:
        if max(m,f) %2 == 1: # max is odd
            g = 1
            s = max(m,f)
        else: # max is even
            g = 3 #(2 min, 1 max)
            s = max(m,f) + 1

    # if diff is 2:
    elif abs(m-f) == 2:
        if m%2 == 1: # both odd
            g = 2 #(2 min)
            s = max(m,f)
        else: #both even
            g = 4 #(3 min, 1 max)
            s = max(m,f) + 1

    # if diff is 3:
    elif abs(m-f) == 3:
        if max(m,f) %2 == 1: # max is odd
            g = 3 #(3 min)
            s = max(m,f)
        else: # max is even
            g = 5 #(4 min, 1 max)
            s = max(m,f) + 1

    # if diff is 4:
    elif abs(m-f) == 4:
        if m%2 == 1: # both are odd
            g = 4 #(4 min)
            s = max(m,f)
        else: # both are even
            g = 6 #(5 min, 1 max)
            s = max(m,f) + 1

    # else diff is 5.
    if max(m,f) %2 == 1: # max is odd
        g = 5 #(5 min)
        s = max(m,f)
    else: # max is even
        g = 7 #(6 min, 1 max)
        s = max(m,f) + 1


    return g, s




###############################################################################

def get_this_event_num():
    """
    Get event number by querying and incrementing highest existing eventNum.
    """

    class Event(Object):
        pass

    q = Event.Query.all().order_by("-eventNum")
    if len(list(q)) == 0:
        return 1
    highest_event_num = list(q)[0].eventNum
    this_event_num = highest_event_num + 1

    return this_event_num

###############################################################################

def make_event_prefix(eventNum):

    return "zE" + ("0"*(4-len(str(eventNum)))) + str(eventNum)

###############################################################################

def main():

    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
    )

    e_num = get_this_event_num()
    prefix = make_event_prefix(e_num)
    print create_event_object("2016.11.05", "19:00", "Palo Alto")

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)










