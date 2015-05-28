"""
The Event class has methods for preparing, simulating, and analyzing an event.

Calling main() simulates an event with 50 men and 50 women.
"""

###############################################################################

# Import Python stuff.
from __future__ import print_function
from pprint import pprint
import itertools
import math
import os
import random
import sys
import time

# Import Parse stuff.
import httplib, json, urllib

# Import ParsePy stuff. ParsePy makes using Parse in Python so much easier.
from parse_rest.connection import ParseBatcher, register, SessionToken
from parse_rest.datatypes import ACL, Function, Object
from parse_rest.role import Role
from parse_rest.user import User

# Import Firebase stuff (https://github.com/mikexstudios/python-firebase)
from firebase import Firebase
import requests

# Import custom functions and classes I've written specifically for Daeious.
from _round import _Round, Round_0, Round_1, Round_2, Round_3, Round_4
from helpers import batch_upload_to_Parse
from helpers import batch_delete_from_Parse_all_objects_of_class


###############################################################################

class Event(Object): pass # needed for Parse Event class interactivity

###############################################################################

class _Event(Object):

    COUNT_EVENT = -1
    STR_EVENT_SERIAL_NUM = ""
    MEN = 0
    WOMEN = 0
    EVENT_DATE = time.strftime("%Y.%m.%d")
    EVENT_TIME = random.choice(["19:00", "19:30", "20:00", "20:30", "21:00"])
    EVENT_LOCATION = random.choice(["Palo Alto", "San Francisco", "Los Angeles"])

    def __init__(self, event_num, num_men, num_women):
        
        _Event.COUNT_EVENT += 1
        _Event.MEN += num_men
        _Event.WOMEN += num_women

        # Calculate Ghosts needed
        mg, fg, s = self.calculate_Ghosts_needed()
        
        self.event_num = event_num
        self.num_men = num_men
        self.num_women = num_women
        self.num_m_ghosts = mg
        self.num_f_ghosts = fg
        self.num_stations = s
        self.num_ipads = s*2

        _Event.STR_EVENT_SERIAL_NUM = "{}{}".format(
            "0"*(4 - len(str(event_num))), event_num)

        # Create a corresponding Event object in Parse upon initialization.
        self.create_event_object_in_Parse()

        # Create event-user (zE_0000_User) objects in Parse upon initialization.
        self.create_event_users_in_Parse()


    def create_event_object_in_Parse(self):
        # Create a corresponding Event object in Parse upon initialization.
        e = Event() # Remember, this is a _Parse_ Event object, so it's ok!
        e.eventNum = self.event_num
        e.eventPrefix = _Event.STR_EVENT_SERIAL_NUM
        e.location = _Event.EVENT_LOCATION
        e.start = [_Event.EVENT_DATE, _Event.EVENT_TIME]
        e.startDate = _Event.EVENT_DATE
        e.startTime = _Event.EVENT_TIME
        e.numMen = _Event.MEN
        e.numWomen = _Event.WOMEN
        e.numUsers = _Event.MEN + _Event.WOMEN
        e.numMaleGhosts = self.num_m_ghosts
        e.numFemaleGhosts = self.num_f_ghosts
        e.numStations = self.num_stations
        e.numIPads = 2*self.num_stations
        e.save()
        pass


    def create_event_users_in_Parse(self):

        # For now, just grab first ones; later, check by array_eventsRegistered.

        """
        Create zE_0000_User objects by "batch_save"-ing them to Parse using 
        ParsePy's ParseBatcher(). Event User objects are _User objects whose 
        array_eventsRegistered contains the eventNum of this current event.

        """

        class zE_0000_User(Object):
            pass

        # # Get the correct class name from the ep = Event Prefix (passed in).
        # eventUser_ClassName = ep + "_User"
        # eventUser_Class = Object.factory(eventUser_ClassName)

        # add some Users to this Event
        qset_all_users = User.Query.all().order_by("userNum")
        li_meu = list(qset_all_users.filter(sex = "M").limit(
            _Event.MEN))
        li_feu = list(qset_all_users.filter(sex = "F").limit(
            _Event.WOMEN))
        li_mgeu = list(qset_all_users.filter(sex = "MG").limit(
            self.num_m_ghosts))
        li_fgeu = list(qset_all_users.filter(sex = "FG").limit(
            self.num_f_ghosts))

        li_users_at_event = li_meu + li_feu + li_mgeu + li_fgeu

        count_eu = len(li_users_at_event)

        li_eu_obj_to_upload = []

        for index, obj_User in enumerate(li_users_at_event):
            new_EU_object = zE_0000_User(
                user_objectId = obj_User.objectId,
                event_userNum = index + 1,
                username = obj_User.username,
                first = obj_User.username.split(" ")[0],
                last = obj_User.username.split(" ")[-1],
                sex = obj_User.sex
            )
            li_eu_obj_to_upload.append(new_EU_object)


        # Batch upload in chunks no larger than 50, 
        # and sleep to avoid timeouts
        batch_upload_to_Parse("zE_0000_User", li_eu_obj_to_upload)    

        pass


    def calculate_Ghosts_needed(self):
        """
        Determine how many ghosts, which lets us know how many stations too.
        This code can probably be significantly cleaned up, but right now I'm just
        gonna get it written.

        A single ghost always goes to the min(m,f).

        m, f must each be >= 20 and <= 50.
        abs(m-f) must be <= 5 (might be low, we'll see).

        """

        # create aliases for code simplicity
        m = _Event.MEN
        f = _Event.WOMEN

        if not ((20 <= m <= 50) and (20 <= f <= 50) and (abs(m-f) <= 5)):
            raise ValueError("m and f must be between 20 and 50 inclusive, and \
                they must differ by no more than 5.")

        g = -1
        s = -1

        # if diff is 0:
        if abs(m-f) == 0:
            if m%2 == 1: # both odd
                g = 0
                s = m
            else: # both even
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
        elif abs(m-f) == 5:
            if max(m,f) %2 == 1: # max is odd
                g = 5 #(5 min)
                s = max(m,f)
            else: # max is even
                g = 7 #(6 min, 1 max)
                s = max(m,f) + 1

        # now determine sexes of ghosts.
        mg = 0
        fg = 0
        if max(m,f) == m:
            fg = abs(m-f)
        else:
            mg = abs(m-f)
        if max(m,f) %2 == 0:
            mg += 1
            fg += 1

        return mg, fg, s


    def simulate(self):
        # simulates an entire event (all 3 rounds, plus pregame and postgame)
        r0 = Round_0()
        r0.prepare()
        pass

###############################################################################

def main():

    # Call "register" to allow parse_rest / ParsePy to work. 
    # --> register(APPLICATION_ID, REST_API_KEY, optional MASTER_KEY)
    register(
        "AKJFNWcTcG6MUeMt1DAsMxjwU62IJPJ8agbwJZDJ", 
        "i8o0t6wg9GOTly0yaApY2c1zZNMvOqNhoWNuzHUS", 
        master_key = "LbaxSV6u64DRUKxdtQphpYQ7kiaopBaRMY1PgCsv"
        )

    this_event = _Event(1, 50, 50)
    this_event.simulate()
    return "Simulation complete."

###############################################################################

if __name__ == '__main__':
    status = main()
    sys.exit(status)























