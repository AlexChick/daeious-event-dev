"""
Queries for a Parse "Event" object with the correct date, time, and location,
then returns its eventNumber
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

###############################################################################

def create_event_object(this_date, this_time, this_location):
    """
    Create an Event object, upload it to Parse, return eventNum.

    Get event number by querying and finding highest existing eventNum. 
    this_date has format "YYYY.MM.DD"
    this_time has format "HH:MM" (24-hour clock)
    this_location is a string (ex, "Palo Alto")
    """

    class Event(Object):
        pass

    q = Event.Query.all().order_by("-eventNum")
    highest_event_num = list(q)[0].eventNum
    this_event_num = highest_event_num + 1

    


    return "Successfully created Event {}.".format(this_event_num)

###############################################################################

def main():

    # Call "register" to allow parse_rest / ParsePy to work. 
    # --> register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
        )

    print create_event_object("2016.11.05", "19:00", "Palo Alto")

    return "\"create_event_object()\" has finished running."

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)










