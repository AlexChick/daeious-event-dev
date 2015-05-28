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

###############################################################################

class _Event(Object):

    COUNT_EVENT = -1
    STR_EVENT_SERIAL_NUM = ""

    def __init__(self, event_num, num_men, num_women):
        self.event_num = event_num
        self.num_men = num_men
        self.num_women = num_women
        _Event.COUNT_EVENT += 1
        num_zeroes = 4 - len(str(event_num))
        _Event.STR_EVENT_SERIAL_NUM = "{}{}".format("0"*num_zeroes, event_num)

    def create_event_object_in_Parse(self):
        class Event(Object): pass
        e = Event()
        e.eventNum = 257
        e.save()
        pass

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























