from __future__ import print_function # has to be on first line or throws error

"""
This program contains several helpful little functions.
"""

###############################################################################
"""                                 IMPORTS                                 """
###############################################################################

# Import Python stuff.
from pprint import pprint
import copy
import itertools
import math
import numpy # for arange or linspace
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

def get_full_QA_list(li_q_nums):

    

    pass

def guys_are_walking(ld, min_distance = 5):

    bool_all_are_walking = False
    num_subrounds = len(ld)
    num_guys = len(ld[0])

    for guy_num in range(1, num_guys+1):
        li_his_station_path = []
        for subround in range(num_subrounds):
            li_his_station_path.append(ld[subround][str(guy_num)])
        for index, station in enumerate(li_his_station_path):
            if station != li_his_station_path[-1]:
                if abs(station - li_his_station_path[index+1]) < min_distance:
                    print("Guy {} ISN'T walking enough!".format(guy_num))
                    return bool_all_are_walking
        print("Guy {} is walking enough.".format(guy_num))

    bool_all_are_walking = True

    return bool_all_are_walking


def optimize_event_timing(
                        m = 40, 
                        w = 40, 
                        min_playing = 30,
                        deviation = 0.5,
                        r1r2_ix_pp_divisor = 4,
                        r2r3_ix_pp_divisor = 10,
                        r1r2_time_multiplier_min = 2,
                        r1r2_time_multiplier_max = 3,
                        r2r3_time_multiplier_min = 2,
                        r2r3_time_multiplier_max = 3
                        ):
    """
    Should each round be the same length of time?
    Should each event? (Yes -- 1 hour)
    Should break times depend on how many people are at the event?
    """

    sec_pregame = 60 * 10 # 600 = 10 minutes
    sec_break_1 = 60 * 5  # 300 = 5 minutes
    sec_break_2 = 60 * 5  # 300 = 5 minutes
    sec_postgame = 60 * 5 # 300 = 5 minutes

    sec_not_playing = sec_pregame + sec_break_1 + sec_break_2 + sec_postgame
    sec_playing = 60*min_playing

    stations = max(m,w) if max(m,w) % 2 == 1 else max(m,w) + 1
    mg = stations - m
    fg = stations - w

    num_r1_ix_pp = int(round(stations/1.0, 0))
    num_r2_ix_pp = int(round(stations/r1r2_ix_pp_divisor, 0)) + 1
    num_r3_ix_pp = int(round(stations/r2r3_ix_pp_divisor, 0)) + 1

    # # make all rounds be the same length, and set sec_per_r1_ix, etc accordingly
    # sec_per_round = sec_playing / 3
    # sec_per_r1_ix = int(sec_per_round / float(num_r1_ix_pp))
    # sec_per_r2_ix = int(sec_per_round / float(num_r2_ix_pp))
    # sec_per_r3_ix = int(sec_per_round / float(num_r3_ix_pp))

    # print ([sec_per_r1_ix, sec_per_r2_ix, sec_per_r3_ix])




    # or, make rounds be specific lengths according to multipliers

    # Make lists of possible per-ix times for each round.
    li_r1_possible_sec_per_ix = numpy.arange(15, 30+1, 0.5)
    li_r2_possible_sec_per_ix = numpy.arange(30, 120+1, 0.5)
    li_r3_possible_sec_per_ix = numpy.arange(60, 300+1, 0.5)

    # Iterate through these lists, adding the good combos to a list to return.
    # "good" means within the deviation
    # "perfect" means exactly equal to playing_time parameter
    lili_good_sec_per_ix_tuples = []
    lili_perfect_sec_per_ix_tuples = []

    for i in li_r1_possible_sec_per_ix:

        r1_sec = i * num_r1_ix_pp

        for j in li_r2_possible_sec_per_ix:
            if (
            float(j)/i >= r1r2_time_multiplier_min
            and
            float(j)/i <= r1r2_time_multiplier_max
            ):

                r2_sec = j * num_r2_ix_pp

                for k in li_r3_possible_sec_per_ix:
                    if (
                    float(k)/j >= r2r3_time_multiplier_min
                    and
                    float(k)/j <= r2r3_time_multiplier_max
                    ):

                        r3_sec = k * num_r3_ix_pp

                        r1r2r3_sec_total = r1_sec + r2_sec + r3_sec

                        if sec_playing - deviation*60 <= r1r2r3_sec_total <= sec_playing + deviation*60:

                            lili_good_sec_per_ix_tuples.append(
                                [
                                (i, j, k), 
                                (r1_sec, r2_sec, r3_sec, r1r2r3_sec_total),
                                (round(float(j)/i, 2), round(float(k)/j, 2))
                                ])

                        if r1r2r3_sec_total == sec_playing:

                            lili_perfect_sec_per_ix_tuples.append(
                                [
                                (i, j, k), 
                                (r1_sec, r2_sec, r3_sec, r1r2r3_sec_total),
                                (round(float(j)/i, 2), round(float(k)/j, 2))
                                ])


    print("Ix per person per round: {}".format((num_r1_ix_pp, num_r2_ix_pp, num_r3_ix_pp)))
    print("Combinations tried: {}".format(
        len(li_r1_possible_sec_per_ix),
        len(li_r2_possible_sec_per_ix),
        len(li_r3_possible_sec_per_ix)))
    print("\nGood combinations: {}".format(len(lili_good_sec_per_ix_tuples)))
    for li_tup in lili_good_sec_per_ix_tuples:
        print(li_tup)
    print("\nPerfect combinations: {}".format(len(lili_perfect_sec_per_ix_tuples)))
    for li_tup in lili_perfect_sec_per_ix_tuples:
        print(li_tup)
    # pprint(lili_perfect_sec_per_ix_tuples)

    return lili_good_sec_per_ix_tuples, lili_perfect_sec_per_ix_tuples






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


def xfrange(first, last, step):
    while first <= last:
        yield first
        first += step


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
    optimize_event_timing()

    pass


if __name__ == "__main__":
    status = main()
    print("\nTesting complete for helpers.py\n")
    sys.exit(status)







