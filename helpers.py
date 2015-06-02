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

def optimize_event_timing(
                        m = 50, 
                        w = 50, 
                        sec_per_r1_ix = 15, 
                        multiplier = 2,
                        minutes_in_entire_event = 60):
    """
    Should each round be the same length of time?
    Should each event?
    Should break times depend on how many people are at the event?
    """

    sec_pregame = 60 * 10 # 600 = 10 minutes
    sec_break_1 = 60 * 5  # 300 = 5 minutes
    sec_break_2 = 60 * 5  # 300 = 5 minutes
    sec_postgame = 60 * 5 # 300 = 5 minutes

    sec_not_playing = sec_pregame + sec_break_1 + sec_break_2 + sec_postgame
    sec_playing = (minutes_in_entire_event * 60) - sec_not_playing

    stations = max(m,w) if max(m,w) % 2 == 1 else max(m,w) + 1
    mg = stations - m
    fg = stations - w

    num_r1_ix_pp = int(round(stations/1.0, 0))
    num_r2_ix_pp = int(round(stations/4.0, 0))
    num_r3_ix_pp = int(round(stations/12.0, 0))

    # make all rounds be the same length, and set sec_per_r1_ix, etc accordingly
    sec_per_round = sec_playing / 3
    sec_per_r1_ix = int(sec_per_round / float(num_r1_ix_pp))
    sec_per_r2_ix = int(sec_per_round / float(num_r2_ix_pp))
    sec_per_r3_ix = int(sec_per_round / float(num_r3_ix_pp))

    print ([sec_per_r1_ix, sec_per_r2_ix, sec_per_r3_ix])

    # make rounds be specific lengths according to multipliers

    #



    return sec_per_r1_ix, sec_per_r2_ix, sec_per_r3_ix



def filter_by_value(sequence, value):
    """
    A generator than yields all elements of a sequence whose attrName 
    matches value.

    More readable than a list comprehension, though accomplishes the same thing.

    http://stackoverflow.com/questions/3013449/list-filtering-list-comprehension-vs-lambda-filter?lq=1
    """
    for element in sequence:
        # for index, att in enumerate(["asdf", "event_number", "ix_num"]):
        #     if hasattr(element, att):
        #         if element.asdf == value \
        #         or element.event_number == value \
        #         or element.ix_num % value == 0:
        #             yield element
        #             pass
                # yield element if element.adsf == value
                # yield element if element.event_number == value
                # yield element if element.ix_num % value == 0

        if hasattr(element, "asdf"):
            if element.adsf == value: 
                yield element

        elif hasattr(element, "event_number"):
            if element.event_number == value:
                yield element

        elif hasattr(element, "ix_num"):
            if element.ix_num % value == 0:
                yield element

        elif hasattr(element, "m_see_f"):
            if element.m_see_f == value:
                yield element



def mk_serial(eNum):
    return "{}{}".format("0"*(4 - len(str(eNum))), eNum)



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
    pass


if __name__ == "__main__":
    status = main()
    print("\nTesting complete for helpers.py\n")
    sys.exit(status)







